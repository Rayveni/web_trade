from sys import path
path.append("...")

#from db_drivers import mongo_manager
from app.attributes import sec_sector
from app.external_sources import tradingview
from .upload_info import update_upload_table_info

def job_sectors(db_manager):

    tv=tradingview()
    err,res=tv.rus_security_sector()
    if err==False:
        return False
    insert_data=[]
    for row in res:
        _descr=row[1]
        for sub_row in row[0]:
            insert_data.append(sec_sector(*sub_row,*_descr))

    res=db_manager.insert_into_table_from_attr('sec_sector',insert_data,bulk=True,rewrite=True)
    res2=update_upload_table_info(db_manager,'sec_sectors',res[1])
 
    return res

