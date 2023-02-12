#from db_drivers import mongo_manager
from app.attributes import securities_short,mosex_sec_history,sec_history_manager_mosex,upload_mosex_sec
from app.external_sources import mosex
from .upload_info import update_upload_table_info
from datetime import datetime
#from pandas import DataFrame
#from .commons import exception
from itertools import chain

def job_mosex_securities(db_manager)->tuple:
    columns= ['DATESTAMP', 'INSTRUMENT_ID', 'LIST_SECTION','SUPERTYPE', 'INSTRUMENT_TYPE', 'INSTRUMENT_CATEGORY', 'TRADE_CODE', 'ISIN', 'REGISTRY_NUMBER', 'REGISTRY_DATE', 'EMITENT_FULL_NAME', 'INN', 'NOMINAL', 'CURRENCY', 'ISSUE_AMOUNT', 'DECISION_DATE', 'OKSM_EDR', 'ONLY_EMITENT_FULL_NAME', 'REG_COUNTRY', 'QUALIFIED_INVESTOR', 'HAS_PROSPECTUS', 'IS_CONCESSION_AGREEMENT', 'IS_MORTGAGE_AGENT', 'INCLUDED_DURING_CREATION', 'SECURITY_HAS_DEFAULT', 'SECURITY_HAS_TECH_DEFAULT', 'INCLUDED_WITHOUT_COMPLIANCE', 'RETAINED_WITHOUT_COMPLIANCE', 'HAS_RESTRICTION_CIRCULATION', 'LISTING_LEVEL_HIST', 'OBLIGATION_PROGRAM_RN', 'COUPON_PERCENT', 'EARLY_REPAYMENT', 'EARLY_REDEMPTION', 'ISS_BOARDS', 'OTHER_SECURITIES', 'DISCLOSURE_PART_PAGE', 'DISCLOSURE_RF_INFO_PAGE']
    df=mosex().securities_list()
    upload_arr=[securities_short(*v.values) for i,v in df[columns].iterrows()]	
    res=db_manager.insert_into_table_from_attr('mosex_securities',upload_arr,bulk=True,rewrite=True)
    res2=update_upload_table_info(db_manager,'mosex_securities',res[1])
    return res



def job_update_sec_hist(db_manager)->tuple:
    now_datetime=datetime.now()
    res=__update_mosex_sec(db_manager,now_datetime)
    return res 
#r=db.find_one('sec_history_manager_mosex',{"secid":'GAZP111'})	 now.strftime("%m")
    #return __db_upload_sec_data(db_manager,'SBER',now_datetime)
    
def __update_mosex_sec(db_manager,start_job):
    sec_list=db_manager.get_table('mosex_securities',query={'list_section':"Первый уровень",
                                                     'supertype':{'$in':['Акции' ,"Депозитарные расписки"
                                                                        ]}
                                                    },
                           columns=['trade_code'],result='json') 
    if sec_list==[]:
        return False,'mosex_securities'                           
    for security_item in sec_list:
        security=security_item['trade_code']
        res=db_manager.insert_into_table_from_attr('upload_mosex_sec',
                                               upload_mosex_sec(trade_code=security,last_updated=start_job),
                                               rewrite=False,
                                               update_criteria={"trade_code":security})     
    return res
def __get_sec_data(security)->tuple:
    res,raw_data=mosex().security_hist(security)
    if res is False:
        return (res,)
    columns=list(map(lambda s:str(s).lower(),raw_data[0]))
    raw_data=list(chain(*raw_data[1]))
    return columns,raw_data


def __db_upload_sec_data(db_manager,security,start_job)->tuple:
    
    res=db_manager.insert_into_table_from_attr('upload_mosex_sec',
                                               upload_mosex_sec(trade_code=security,last_updated=start_job),
                                               rewrite=False,
                                               update_criteria={"trade_code":security})    
    
    
    columns,raw_data=__get_sec_data(security)
    columns=list(map(lambda s:s.lower(),columns))
    boardid_ind=columns.index('boardid')
    raw_data=list(filter(lambda row: row[boardid_ind] =='TQBR', raw_data))
    

    tradedate_ind=columns.index('tradedate')
    shortname_ind=columns.index('shortname')
    secid_ind=columns.index('secid')
    numtrades_ind=columns.index('numtrades')
    value_ind=columns.index('value')
    open_ind=columns.index('open')
    low_ind=columns.index('low')
    high_ind=columns.index('high')
    legalcloseprice_ind=columns.index('legalcloseprice')
    waprice_ind=columns.index('waprice')
    close_ind=columns.index('close')
    volume_ind=columns.index('volume')
    marketprice2_ind=columns.index('marketprice2')
    marketprice3_ind=columns.index('marketprice3')
    admittedquote_ind=columns.index('admittedquote')
    mp2valtrd_ind=columns.index('mp2valtrd')
    marketprice3tradesvalue_ind=columns.index('marketprice3tradesvalue')
    admittedvalue_ind=columns.index('admittedvalue')
    waval_ind=columns.index('waval')
    tradingsession_ind=columns.index('tradingsession')

    date_list=[]
    for row in raw_data:
        date_trade=datetime.strptime(row[tradedate_ind],'%Y-%m-%d')
        date_list.append(date_trade)
        ticker=row[secid_ind]
        insert_row=mosex_sec_history(
                                            boardid=row[boardid_ind],
                                            tradedate=date_trade,
                                            shortname=row[shortname_ind],
                                            secid=ticker,
                                            numtrades=row[numtrades_ind],
                                            value=row[value_ind],
                                            open_price=row[open_ind],
                                            low=row[low_ind],
                                            high=row[high_ind],
                                            legalcloseprice=row[legalcloseprice_ind],
                                            waprice=row[waprice_ind],
                                            close=row[close_ind],
                                            volume=row[volume_ind],
                                            marketprice2=row[marketprice2_ind],
                                            marketprice3=row[marketprice3_ind],
                                            admittedquote=row[admittedquote_ind],
                                            mp2valtrd=row[mp2valtrd_ind],
                                            marketprice3tradesvalue=row[marketprice3tradesvalue_ind],
                                            admittedvalue=row[admittedvalue_ind],
                                            waval=row[waval_ind],
                                            tradingsession=row[tradingsession_ind]                                                                                                                                                 
                                            )
        
     
        res=db_manager.insert_into_table_from_attr('mosex_sec_history',
                                                   insert_row,
                                                   rewrite=False,
                                                   update_criteria={"secid":ticker,
                                                                    "tradedate":date_trade}
                                                  )  
    upd_hist=sec_history_manager_mosex(ticker=ticker,
                                       sec_name=row[shortname_ind],
                                       start_date=min(date_list),
                                       end_date=max(date_list),
                                       actual_for=start_job)
    res2=db_manager.insert_into_table_from_attr('sec_history_manager_mosex',
                                                upd_hist,
                                                update_criteria={"secid":ticker})
                                                
    res3=db_manager.insert_into_table_from_attr('upload_mosex_sec',
                                                upload_mosex_sec(trade_code=security,last_updated=start_job,success=True),
                                                update_criteria={"trade_code":security})                                                
                                                
    #res2=update_upload_table_info(db_manager,'job_world_fond_indexes',res[1])          

    return res,res2#columns,raw_data