import lxml.html as lh
import re
from .base_session import request_session

class tradingview(request_session):
    __slots__='url','sources'
    def __init__(self):
        self.url:str=r'https://ru.tradingview.com'
        self.sources:dict={'rus_sectorandindustry':r'/markets/stocks-russia/sectorandindustry-industry/'
                          }                           

    def __transform_str(self,text):
        return text.replace('\t','').replace('\n','')

    def parse_sector(self,sector_url,session) :

        _sector_url=self.url+sector_url
        page=session.get(_sector_url)   

        doc = lh.fromstring(page.content)
        table_body = doc.xpath('//tbody[@class="tv-data-table__tbody"]')[0]
        r=[]
        for row  in table_body.getchildren():
            _list=row[0].text_content().split('\t')[20:]
            _extract=[]
            for el in _list:
                _el=self.__transform_str(el)
                if len(_el)>0:
                    _extract.append(_el)
            r.append([*_extract,row[4].text_content()])              

            
        return (sector_url,r)
            
    
    def rus_security_sector(self)->tuple:
        s=self._init_session()
        page=s.get(self.url+self.sources['rus_sectorandindustry'])   
        doc = lh.fromstring(page.content)
      
        table_body = doc.xpath('//tbody[@class="tv-data-table__tbody"]')[0]    
        extract_r=lambda _row:list(map(lambda f:self.__transform_str(f.text_content()),[_row[0],_row[-2]]))      
        _urls={row.xpath('.//@href')[0]:extract_r(row) for row in table_body.getchildren()}
        _worker=lambda url:self.parse_sector(url,s)
        
        err,res=self._start_pool(s,_worker,list(_urls.keys())) 

        if not err:
            return (False,)
        else:
            return (True,[[row[1],_urls[row[0]]] for row in res])
