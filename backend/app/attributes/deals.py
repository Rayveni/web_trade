class deals:
    __slots__ ='ticker','sec_name','timestamp','bought','sold','price_currency','price','trans_currency','trans_volume','trans_nkd','broker_fee','broker_fee_currency','calc_volume','calc_cnt'
    
    def __init__(self,ticker:str,
                 sec_name,
                 timestamp,
                 bought:int,
                 sold:int,
                 price_currency:str,
                 price:float,
                 trans_currency:str,
                 trans_volume:float,
                 trans_nkd:float,
                 broker_fee:float,
                 broker_fee_currency:str):
        _to_float=lambda t:0 if t=='-' else float(t)				 
        self.sec_name=sec_name
        self.timestamp=timestamp
        self.bought=_to_float(bought)
        self.sold=_to_float(sold)
        self.ticker=ticker
        self.price_currency=price_currency
        self.price=_to_float(price)
        self.trans_currency=trans_currency
        self.trans_volume=_to_float(trans_volume)
        self.trans_nkd=_to_float(trans_nkd)
        self.broker_fee=_to_float(broker_fee)
        self.broker_fee_currency=broker_fee_currency
        self.calc_volume=round(self.trans_volume+  self.broker_fee  if self.bought>0 else -self.trans_volume+self.broker_fee,2)
        self.calc_cnt=self.bought-self.sold 		