from os import getenv
from  redis import from_url
from rq import Queue
from rq.job import Job

class background_tasks:
    __slots__ ='_queue','conn'
    def __init__(self,queue_name='default'):  
        redis_url = getenv('redis_url')
        self.conn = from_url(redis_url)
        self._queue = Queue(name=queue_name,connection=self.conn)
        
    def add_task(self,task,*args,**kwargs):
        self._queue.enqueue(task,*args,**kwargs)
 
    def queue_jobs(self,registry:str):
        """
        failed_job_registry
        started_job_registry
        finished_job_registry
        deferred_job_registry
        scheduled_job_registry
        canceled_job_registry
        """
        job_registry=eval("self._queue.{}".format(registry))
        job_ids=job_registry.get_job_ids()
        _jobs=[Job.fetch(_job_id, connection=self.conn) for _job_id in job_ids]
        return _jobs