from app.db_drivers import mongo_manager
from .config_manager import get_config

def init_db_manager():   
    config={k:v for (k,v) in get_config().items() if k in ['db_url','db_name'] }   
    return mongo_manager(config)