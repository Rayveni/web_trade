class index_value:
    __slots__='index_id','date','currency','open_price','min_price','max_price','close_price','volume','capitalization','duration','profit'
    def __init__(self,index_id,date,currency,open_price,min_price,max_price,close_price,volume,capitalization,duration,profit):
        self.index_id=index_id
        self.date=date
        self.currency=currency
        self.open_price=open_price
        self.min_price=min_price
        self.max_price=max_price
        self.close_price=close_price
        self.volume=volume
        self.capitalization=capitalization
        self.duration=duration
        self.profit=profit