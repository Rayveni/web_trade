from functools import partial
from .base_session import request_session
class alphavantage(request_session):
    __slots__='url','sources','token'
    def __init__(self,token):
        self.url:str=r'https://www.alphavantage.co/'
        self.__token=token       
        self.sources:dict={'daily':r'query?function=TIME_SERIES_DAILY'
                          }                    
      
    def __fond_index_history_worker(self,session,url:str,params:dict,ticker:str)->tuple:
        print(ticker,url)	
        print(params)
        response=session.get(url , params = {'symbol' :ticker,**params})
        if response.ok:
            return True,response.json()
        return (False,ticker)

    def fond_index_history(self,tickers_list:list,full_reload:bool=True,n_threads:int=7)->tuple:
        if full_reload:
            outputsize='full'
        else:
            outputsize='compact'
        params={'outputsize':outputsize,'apikey':self.__token}
        s=self._init_session()        
        worker=partial(self.__fond_index_history_worker,s,self.url+self.sources['daily'],params)  
        
        err,res=self._start_pool(s,worker,tickers_list)      
        if not err:
            return (False,)
        return True,res

