class fond_index_history:
    __slots__='index_id','date','year','currency','open_price','min_price','max_price','close_price','volume'
    def __init__(self,index_id,date,year,currency,open_price,min_price,max_price,close_price,volume):
        self.index_id=index_id
        self.year=year		
        self.date=date
        self.currency=currency
        self.open_price=open_price
        self.min_price=min_price
        self.max_price=max_price
        self.close_price=close_price
        self.volume=volume