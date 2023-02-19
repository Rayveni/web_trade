#http://iss.moex.com/iss/reference/
#http://iss.moex.com/iss/securitygroups/stock_index/collections
from functools import partial
from .base_session import request_session
from time import sleep
from pandas import read_csv
from functools import partial


class mosex(request_session):
    __slots__ = ['base_url','references_dict','return_data_type','error','tries_limit','tries_pause','tries_in_seq','full_urls']
    def __init__(self):
        self.base_url = r'http://iss.moex.com/iss/'
        self.full_urls={'securities_list':r'https://www.moex.com/ru/listing/securities-list-csv.aspx?type=2'}
        self.references_dict ={'securities_list':{'link':'securities'
                                                 ,'chunk':False},
                               'global_dict':{'link':r'index'
                                               ,'chunk':False}
                                ,'security_spec':{'link':r'securities/{r[security]}'
                                                  ,'chunk':False}
                                ,'security_history':{'link':r'history/engines/{r[engine]}/markets/{r[market]}/securities/{r[security]}'
                                                     ,'chunk':True}
                               ,'index_list':{'link':r'statistics/engines/stock/markets/index/analytics'
                                             , 'chunk':False}
                               }
        self.return_data_type='json'
        self.tries_limit=1000
        self.tries_pause=10
        self.tries_in_seq=8		
        
    def __url_construct(self,reference,params=None):
 
        url='{0}{1}.{2}'.format(self.base_url,self.references_dict[reference]['link'],self.return_data_type)
        if params is not None:
            url=url.format(r=params)
        return url
          
    def securities_list(self):	
        return read_csv(self.full_urls['securities_list'],sep=';',encoding='cp1251')   



    def __security_hist_worker(self,session,url,params,start):
        return session.get(url , params = {**params,**{'start':start}}).json()['history']['data']

    def security_hist(self,security,engine:str='stock',market:str='shares',date_from='2016-01-01',n_threads=7):
        url=self.__url_construct('security_history'
                                 ,params={'engine':engine
                                          ,'market':market
                                          ,'security':security}
                                 )
        query_params={'from':date_from}
        s = self._init_session()
        response=s.get(url , params = query_params).json()
        
        columns=response['history']['columns']
        start_cursor,end_cursor,step=response['history.cursor']['data'][0]
        worker=partial(self.__security_hist_worker,s,url,query_params)
       		
        err,res=self._start_pool(s,
                                 worker,
                                 _worker_args=[i for i in range(start_cursor,end_cursor,step)],
                                 n_threads=7,
                                 n_tries=6,
                                 sleep_interval=1)


        return err,(columns,res)		
#iis.__url_construct('security_spec',{'security':'RTSog'})
#r=iis.query('security_spec',{'security':'RTSog'})
#r=iis.security_hist('RTSog','stock','index',n_threads=7)
#iis.security_hist('RTSFN','stock','index',n_threads=7,date_from='2016-01-01')
#iis.security_hist('GAZP','stock','shares',n_threads=7,date_from='2016-01-01')