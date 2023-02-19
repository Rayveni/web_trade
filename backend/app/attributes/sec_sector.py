class sec_sector:
    __slots__ ='ticker','sec_name','action','industry','sector'
    def __init__(self,ticker:str,sec_name:str,action:str,industry:str,sector:str):
        self.ticker=ticker
        self.sec_name=sec_name
        self.action=action
        self.industry=industry
        self.sector=sector