from app.attributes import sec_history_manager,fond_index_history
from app.external_sources import alphavantage
from time import sleep
from datetime import datetime
from .upload_info import update_upload_table_info

def _process_data(_data)->tuple:
    print(_data)
    meta_data=_data['Meta Data']
    _symbol,last_refreshed=meta_data['2. Symbol'],meta_data['3. Last Refreshed']
    res,date_list={},[]
    for key,_value in _data['Time Series (Daily)'].items():
        value={'date':key,**_value}
        _year=int(key[:4])
        date_list.append(datetime.strptime(key, '%Y-%m-%d'))      
        try:
            temp=res[_year]
            temp.append(value)
        except:
            res[_year]=[value]

    return _symbol,last_refreshed,res,min(date_list),max(date_list)
    
def job_world_fond_indexes(db_manager):
    refresh_years=3
    alphavantage_token=db_manager.find_one('api_tokens',
                                           query={ 'key': { '$eq': 'alphavantage' } },
                                           return_fields=['value'])['value']
    history_manager=db_manager.get_table('sec_history_manager',result='dict',dict_key='ticker')                                           
    _indexes={'.INX':{'key':'S&P 500' ,'description':'индекс в который входят 500 крупнейших по капитализации компаний США.'},
             '.DJI' :{'key':'DJI','description':'промышленный индекс Доу-Джонса. Наверное самый популярный индекс в мире. В состав входит 30 крупнейших компаний США' },
             '^N225' :{'key':'Nikkei 225' , 'description':'японский индекс, куда входит 225 компаний. Ежегодно состав пересматривается. В него входят такие гиганты, как Honda, Panasonic, Mazda и прочие. С вероятностью 99,9% все японские бренды, которые вы знаете входят в NIKKEI 225.  Подобно S&P 500, довольно объективно отражает состояние экономики. Наиболее важный индекс в Азиатском регионе'}, 
             '^GDAXI':{'key':'DAX','description':'германский биржевой индекс, куда входит 30-ка самых главных компаний страны: Adidas, BMW, Henkel,Volkswagen и прочие.'},
             '^FTSE':{'key':'FTSE 100' ,'description':'наиболее уважаемый и котируемый индекс на европейских площадках. В составе 100 крупнейших компаний, торгуемых на Лондонской фондовой бирже.'},
             '000001.SS':{'key':'000001.SS','description':'крупнейшая торговая площадка континентального Китая, одна из лидирующих азиатских бирж.'}        
        }      
    chunk_len,_indexes_list,res=5,list(_indexes.keys()),[]
    alp_v=alphavantage(alphavantage_token)  
    for i in range(0, len(_indexes_list), chunk_len):
        err,r=alp_v.fond_index_history(_indexes_list[i:i + chunk_len])
        if err==False:
            return False
        res+=r
        if len(_indexes_list)>i+chunk_len:
            sleep(60)
    
    hist_upd,sec_insert=[],[] 
    for  _el in res:
        _ticker,_last_refreshed,_data_arr,min_date_list,max_date_list=_process_data(_el)
        hist_upd.append(sec_history_manager(_ticker,
                                            sec_name='',
                                            currency='',
                                            start_date=min_date_list,
                                            end_date=max_date_list,
                                            actual_for=_last_refreshed))
        for key,value in _data_arr.items():
            if _ticker in history_manager.keys():
                if key >history_manager[_ticker]['end_date'].year-refresh_years:
                    db_manager.insert_into_table_from_attr('fond_index_history',
                                                           fond_index_history(ticker=_ticker,
                                                                              year=key,
                                                                              history=value),
                                                           bulk=False,rewrite=False,update_criteria={"ticker":_ticker,'year':key})
            else:
                sec_insert.append(fond_index_history(ticker=_ticker,year=key,history=value))
			


    if len(sec_insert)>0:
        res3=db_manager.insert_into_table_from_attr('fond_index_history',sec_insert,bulk=True,rewrite=True)           
    res=db_manager.insert_into_table_from_attr('sec_history_manager',hist_upd,bulk=True,rewrite=True)
    res2=update_upload_table_info(db_manager,'job_world_fond_indexes',res[1])    
    return res
