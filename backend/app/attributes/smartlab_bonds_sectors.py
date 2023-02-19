class smartlab_bonds_sectors:
    __slots__ ='ticker','sector','data'
    def __init__(self,ticker:str,sector:str,data:str):
        self.ticker=ticker
        self.sector=sector
        self.data=data