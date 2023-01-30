class assets:
    __slots__ ='ticker','sec_name','asset_type','date','amount','value','nkd','price_currency'
    def __init__(self,ticker:str,sec_name,asset_type,date,amount,value,nkd,price_currency):
        _to_float=lambda t:0 if t=='-' else float(t)	
        self.sec_name=sec_name
        self.asset_type=asset_type
        self.date=date
        self.amount=_to_float(amount)
        self.ticker=ticker
        self.value=_to_float(value)
        self.nkd=_to_float(nkd)
        self.price_currency=price_currency

