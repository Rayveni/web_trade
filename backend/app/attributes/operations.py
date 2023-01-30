class operations:
    __slots__ ='tiker','sec_name','asset_type','date','bought','sold','currency','value','aci','commission','commission_cur'
    def __init__(self,tiker:str,sec_name:str,asset_type:str,date,bought:int,sold:int,currency,value:float,
                 aci:float,commission:float,commission_cur):
        _to_float=lambda t:0 if t=='-' else float(t)				 
        self.tiker=tiker
        self.sec_name=sec_name
        self.asset_type=asset_type
        self.date=date
        self.bought=_to_float(bought)
        self.sold=_to_float(sold)
        self.currency=currency
        self.value=value
        self.aci=aci
        self.commission=_to_float(commission)
        self.commission_cur=commission_cur