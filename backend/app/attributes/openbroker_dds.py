class openbroker_dds:
    __slots__ ='date','currency','sum','description'
    def __init__(self,date:str,currency:str,sum:float,description:str):
        self.date=date
        self.currency=currency
        self.sum=sum
        self.description=description
 