class sec_history_manager_mosex:
    __slots__ ='ticker','sec_name','start_date','end_date','actual_for'
    def __init__(self,ticker:str,sec_name:str,start_date:str,end_date:str,actual_for:str):
        self.ticker=ticker
        self.start_date=start_date
        self.sec_name=sec_name         

        self.end_date=end_date
        self.actual_for=actual_for