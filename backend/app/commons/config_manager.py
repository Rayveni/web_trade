from os import getenv

def get_config():
    db_url=getenv('mongo_url')
    db_name=getenv('mongo_work_db')    
    config={'db_url':db_url,'db_name':db_name}    
    return config