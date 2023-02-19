from requests import Session
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
from functools import partial
class request_session:
    def _init_session(self):
        s = Session()
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
        return s

    def _thread_pool(self,worker,arg_list:list,n_threads:int)->tuple:

        true_results,false_results=[],[]
        pool = ThreadPool(n_threads)
        results=pool.map(worker,arg_list)
        pool.close()
        pool.join()

        for el in results:
            if el[0]:
                true_results.append(el[1])
            else:
		
                false_results.append(el[1])
        return (true_results,false_results)       

    def __worker_wrapper(self,f,*args):
        try:	
            res=f(*args)				
            return (True,res)
        except:
            return (False,)			



    def _start_pool(self,session,_worker,_worker_args:list,n_threads:int=7,n_tries:int=6,sleep_interval:int=1)->tuple:
        true_results_final,i=[],0
        while i < n_tries:
            true_results,false_results=self._thread_pool(partial(self.__worker_wrapper,_worker),_worker_args,n_threads=n_threads)
            true_results_final=true_results+true_results_final
            if len(false_results)==0:
                break
            worker_args=false_results[1]
            sleep(sleep_interval)
            i+=1

        session.close()
        if len(false_results)>0:
            return (False,)
        else:
            return (True,true_results_final)