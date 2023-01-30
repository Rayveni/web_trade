class upload_mosex_sec:
    __slots__='trade_code','last_updated','success'
    def __init__(self,trade_code:str,last_updated,success:bool=False):
        self.trade_code=trade_code
        self.success=success
        self.last_updated=last_updated