class avg_assets:
    __slots__ ='ticker','value','total_sum','total_cnt'
    def __init__(self,ticker:str,total_sum:float,total_cnt:float):
        self.ticker=ticker
        self.total_sum=round(total_sum,2)
        self.total_cnt=total_cnt
        self.value=round(total_sum/total_cnt,2)