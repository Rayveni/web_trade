#from db_drivers import mongo_manager
from app.attributes import sec_history_manager,fond_index_history
from app.external_sources import yahoo_finance
from time import sleep
from .upload_info import update_upload_table_info
from datetime import datetime

sleep_sec=60

def _extract_data(data):
    _data=data['chart']['result'][0]
    meta=_data['meta']
    symbol,currency=meta['symbol'],meta['currency']
    _timestamp=[datetime.fromtimestamp(el) for el in _data['timestamp']]
    indicators=_data['indicators']['quote'][0]
    n=len(_timestamp)
    return [[fond_index_history(symbol,
                               _timestamp[i],
                               _timestamp[i].year,							   
                               currency,
                               indicators['open'][i],
                               indicators['low'][i],
                               indicators['high'][i],
                               indicators['close'][i],
                               indicators['volume'][i]) 
            for i in range(n)],symbol,currency,min(_timestamp),max(_timestamp)]

def job_yahoo(db_manager)->tuple:
    yf=yahoo_finance()
    _indexes={'^GSPC':{'key':'S&P 500' ,'description':'индекс в который входят 500 крупнейших по капитализации компаний США.'},
             '^DJI' :{'key':'DJI','description':'промышленный индекс Доу-Джонса. Наверное самый популярный индекс в мире. В состав входит 30 крупнейших компаний США' },
             '^N225' :{'key':'Nikkei 225' , 'description':'японский индекс, куда входит 225 компаний. Ежегодно состав пересматривается. В него входят такие гиганты, как Honda, Panasonic, Mazda и прочие. С вероятностью 99,9% все японские бренды, которые вы знаете входят в NIKKEI 225.  Подобно S&P 500, довольно объективно отражает состояние экономики. Наиболее важный индекс в Азиатском регионе'}, 
             'DAX':{'key':'DAX','description':'германский биржевой индекс, куда входит 30-ка самых главных компаний страны: Adidas, BMW, Henkel,Volkswagen и прочие.'},
             '^FTSE':{'key':'FTSE 100' ,'description':'наиболее уважаемый и котируемый индекс на европейских площадках. В составе 100 крупнейших компаний, торгуемых на Лондонской фондовой бирже.'},
             '000001.SS':{'key':'000001.SS','description':'крупнейшая торговая площадка континентального Китая, одна из лидирующих азиатских бирж.'}
             }  
    
    chunk_len,_indexes_list,res=5,list(_indexes.keys()),[]
 
    for i in range(0, len(_indexes_list), chunk_len):
        err,r=yf.ticker_history(_indexes_list[i:i + chunk_len])
        if err==False:
            return False
        res+=r
        if len(_indexes_list)>i+chunk_len:
            sleep(sleep_sec)
    table_data,table_info=[],[]
    for table_chunk in res:
        _chunk,symbol,currency,min_d,max_d=_extract_data(table_chunk)
        table_data+=_chunk
        table_info.append(sec_history_manager(symbol,_indexes[symbol]['key'],currency,min_d,max_d,max_d,_indexes[symbol]['description']))

    if len(table_data)>0:
        res2=db_manager.insert_into_table_from_attr('fond_index_history',table_data,bulk=True,rewrite=True)           
    res=db_manager.insert_into_table_from_attr('sec_history_manager',table_info,bulk=True,rewrite=True)
    res2=update_upload_table_info(db_manager,'job_world_fond_indexes',res[1])  

    return res

