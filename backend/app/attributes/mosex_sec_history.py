class mosex_sec_history:
    __slots__='boardid','tradedate','shortname','secid','numtrades','value','open_price','low','high','legalcloseprice','waprice','close','volume','marketprice2','marketprice3','admittedquote','mp2valtrd','marketprice3tradesvalue','admittedvalue','waval','tradingsession'
    def __init__(self,boardid,tradedate,shortname,secid,numtrades,value,open_price,low,high,legalcloseprice,waprice,close,volume,marketprice2,marketprice3,admittedquote,mp2valtrd,marketprice3tradesvalue,admittedvalue,waval,tradingsession):
        self.boardid=boardid
        self.tradedate=tradedate
        self.shortname=shortname
        self.secid=secid
        self.numtrades=numtrades
        self.value=value
        self.open_price=open_price
        self.low=low
        self.high=high
        self.legalcloseprice=legalcloseprice
        self.waprice=waprice
        self.close=close
        self.volume=volume
        self.marketprice2=marketprice2
        self.marketprice3=marketprice3
        self.admittedquote=admittedquote
        self.mp2valtrd=mp2valtrd
        self.marketprice3tradesvalue=marketprice3tradesvalue
        self.admittedvalue=admittedvalue
        self.waval=waval
        self.tradingsession=tradingsession