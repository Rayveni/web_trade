class sec_history_manager:
    __slots__ ='ticker','sec_name','currency','start_date','end_date','actual_for','description'
    def __init__(self,ticker:str,sec_name:str,currency:str,start_date:str,end_date:str,actual_for:str,description:str):
        self.ticker=ticker
        self.start_date=start_date
        self.sec_name=sec_name         
        self.currency=currency  
        self.end_date=end_date
        self.description=description
        self.actual_for=actual_for