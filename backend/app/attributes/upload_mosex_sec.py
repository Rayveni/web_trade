class upload_mosex_sec:
    __slots__='trade_code','last_updated','success','start_date','end_date'
    def __init__(self,trade_code:str,last_updated,start_date,end_date,success:bool=False):
        self.trade_code=trade_code
        self.success=success
        self.last_updated=last_updated
        self.start_date=start_date        
        self.end_date=end_date