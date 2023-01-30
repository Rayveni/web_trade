#from db_drivers import mongo_manager
from app.attributes import smartlabbondsusd,smartlabbondsrur
from app.external_sources import smartlab
from .upload_info import update_upload_table_info
from datetime import datetime

def __str_to_date(_date:str,_format:str='%Y-%m-%d'):
    if _date=='0000-00-00':
        _date='2111-01-01'
    return datetime.strptime(_date,_format)

def __optional_attr_id(_arr:list,_item:str)->tuple:
    try:
        res=_arr.index(_item)
    except:
        res=None
    return res 

def __none_value(_arr,_id):
    if _id is None:
        return None
    else:
        return _arr[_id]
    
def transform_rur_bonds(columns:list,data:list,bond_group:str)->list:
 
    ticker_id=columns.index('Тикер')
    last_deal_id=columns.index('Время')
    sec_name_id=columns.index('Имя')
    redemption_id=columns.index('Погашение')
    oferta_id=__optional_attr_id(columns,'Оферта')
    years_till_redemption_id=columns.index('Лет допогаш.')
    pers_profit_id=columns.index( 'Доходн')
    duraction_years_id=columns.index( 'Дюр-я, лет')
    ofz_id=__optional_attr_id(columns,'Тип ОФЗ')
    annual_bond_pers_profit_id=columns.index( 'Год.куп.дох.')
    last_deals_bond_pers_profit_id=columns.index( 'Куп.дох.посл.')
    price_id=  columns.index('Цена')
    volume_rur_mln_id=columns.index('Объем,млн руб')
    bond_rur_id=columns.index('Купон, руб')
    frequency_in_year_id=columns.index('Частота,раз в год')
    nkd_rur_id=columns.index('НКД, руб')
    bond_date_id=columns.index('Дата купона')
    res=[]
    for row in data:
        res.append(smartlabbondsrur(bond_category=bond_group, 
                                    ticker=row[ticker_id][0].split('/')[-2],
                                    last_deal=row[last_deal_id],
                                    sec_name=row[sec_name_id], 
                                    redemption=__str_to_date(row[redemption_id]), 
                                    oferta=  __none_value(row,oferta_id),
                                    years_till_redemption=row[years_till_redemption_id],                        
                                    pers_profit=row[pers_profit_id],
                                    duraction_years=row[duraction_years_id],
                                    ofz_type=__none_value(row,ofz_id),
                                    annual_bond_pers_profit=row[annual_bond_pers_profit_id],
                                    last_deals_bond_pers_profit=row[last_deals_bond_pers_profit_id],
                                    price=row[price_id],
                                    volume_rur_mln=row[volume_rur_mln_id],
                                    bond_rur=row[bond_rur_id],
                                    frequency_in_year=row[frequency_in_year_id],
                                    nkd_rur=row[nkd_rur_id], 
                                    bond_date=row[bond_date_id]))
    return res
        
        
def transform_usd_bonds(columns:list,data:list,bond_group:str)->list:
    ticker_id=columns.index('Тикер')
    last_deal_id=columns.index('Время')
    sec_name_id=columns.index('Имя')
    redemption_id=columns.index('Погашение')
    oferta_id=__optional_attr_id(columns,'Оферта')
    years_till_redemption_id=columns.index('Лет допогаш.')
    pers_profit_id=columns.index( 'Доходн')
    #duraction_years_id=columns.index( 'Дюр-я, лет')
    #ofz_id=__optional_attr_id(columns,'Тип ОФЗ')
    annual_bond_pers_profit_id=columns.index( 'Год.куп.дох.')
    last_deals_bond_pers_profit_id=columns.index( 'Куп.дох.посл.')
    price_id=  columns.index('Цена')
    volume_thousand_usd_id=columns.index('Объем, тыс.')
    bond_usd_id=columns.index('Купон')
    frequency_in_year_id=columns.index('Частота,раз в год')
    nkd_usd_id=columns.index('НКД')
    bond_date_id=columns.index('Дата купона')
    res=[]
    for row in data:
        res.append(smartlabbondsusd(bond_category=bond_group, 
                                    ticker=row[ticker_id][0].split('/')[-2],
                                    last_deal=row[last_deal_id],
                                    sec_name=row[sec_name_id], 
                                    redemption=__str_to_date(row[redemption_id]), 
                                    oferta=  __none_value(row,oferta_id),
                                    years_till_redemption=row[years_till_redemption_id],                        
                                    pers_profit=row[pers_profit_id],
                                    #duraction_years=row[duraction_years_id],
                                    #ofz_type=__none_value(row,ofz_id),
                                    annual_bond_pers_profit=row[annual_bond_pers_profit_id],
                                    last_deals_bond_pers_profit=row[last_deals_bond_pers_profit_id],
                                    price=row[price_id],
                                    volume_thousand_usd=row[volume_thousand_usd_id],
                                    bond_usd=row[bond_usd_id],
                                    frequency_in_year=row[frequency_in_year_id],
                                    nkd_usd=row[nkd_usd_id], 
                                    bond_date=row[bond_date_id]))
    return res        

def job_sl_bonds(db_manager)->tuple:
    sm=smartlab()
    res=sm.bonds_info()
    insert_rur_data=[]
    insert_usd_data=[]
    for key,value in res.items():    
        _columns=[el if el!='Unnamed: 1' else 'Время' for el in value[0]]
     
        if value[2]=='USD':
            insert_usd_data+=transform_usd_bonds(_columns,value[1],key)
        else:
            if key=='ОФЗ':
                _columns=[el if el!='!' else 'Тип ОФЗ' for el in _columns]
            _columns=[el if el!='Объем, млн руб' else 'Объем,млн руб' for el in _columns]    
            insert_rur_data+=transform_rur_bonds(_columns,value[1],key)        


    res=db_manager.insert_into_table_from_attr('smartlabbondsrus',insert_rur_data,bulk=True,rewrite=True)
    res2=update_upload_table_info(db_manager,'smartlabbondsrus',res[1])
    res3=db_manager.insert_into_table_from_attr('smartlabbondsusd',insert_usd_data,bulk=True,rewrite=True)
    res4=update_upload_table_info(db_manager,'smartlabbondsusd',res3[1])
 
    return res,res3
