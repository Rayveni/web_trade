from functools import partial
from .base_session import request_session
class yahoo_finance(request_session):
    __slots__='_base_url','sources','max_period','min_period'
    def __init__(self):
        self._base_url:str = r'https://query1.finance.yahoo.com'     
        self.sources:dict={'history':r"{base_url}/v8/finance/chart/{ticker}"
                          } 
        self.max_period=4102434000 #'2100-01-01'
        self.min_period=631141200  #'1990-01-01'
      
    def __ticker_history_worker(self,session,params:dict,ticker:str)->tuple:
        url=self.sources['history'].format(base_url=self._base_url,ticker=ticker)

        response=session.get(url , params = {**params})

        return response.json()

    def ticker_history(self,tickers_list:list,n_threads:int=7)->tuple:

        s=self._init_session()
        params={"interval":'1d'}    
        params["period1"]=self.min_period
        params["period2"]=self.max_period
        worker=partial(self.__ticker_history_worker,s,params)  
        
        err,res=self._start_pool(s,worker,tickers_list)      
        if not err:
            return (False,)
        return True,res

