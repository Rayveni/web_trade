from .base_session import request_session
import lxml.html as lh
from collections import Counter
#import datetime
#from lxml import etree
#print(etree.tostring(tr_elements[-1][2], pretty_print=True))
class smartlab(request_session):
    __slots__='sources','link'
    def __init__(self):
        self.link:str=r'https://smart-lab.ru'
        self.sources:dict={'bonds':{'ОФЗ':{'link':r'/q/ofz/','currency':'RUR','paging':None},
                               'Муниципальные':{'link':r'/q/subfed/','currency':'RUR','paging':None},
                               'Корпоративные':{'link':r'/q/bonds/','currency':'RUR'
                                                ,r'paging':'order_by_val_to_day/desc/page{}/'},
                               'Еврооблигации':{'link':r'/q/eurobonds/','currency':'USD','paging':None}
                              },
                           'bonds_query':r'/q/bonds/'
                           
                     }
        self.limit_pages=100

    def __table_from_html(self,url:str,extra_fields_dict:dict=None)->tuple:
        mask="Unnamed: {}"
        """
        extra_fields_dict={field_text_val:[{'add_column_name':0,'xpath_text':"a/@href",'insert_position':0}]}
        """
        with self._init_session() as s:
            page=s.get(url)
        doc = lh.fromstring(page.content)
        tr_elements = doc.xpath('//tr')
        header=[h.text_content() for h in tr_elements[0]]
        ununique_columns=[ key for key,value in Counter(header).items() if value>1]
        if len(ununique_columns)>0:
            for i in range(len(header)):
                if header[i] in ununique_columns:
                    header[i]=mask.format(i)
                
        if extra_fields_dict:
            keys= list(extra_fields_dict.keys())
            for key in keys:
                value=extra_fields_dict[key]

                extra_fields_dict[header.index(key)]=extra_fields_dict.pop(key)
                for condition in value:
                    header.insert(condition['insert_position'],condition['add_column_name'])

        res=[]

        for row in tr_elements[1:]:           
            arr=[el.text_content() for el in row]
            if len(arr)>1:
                if extra_fields_dict:
                    for key,value in extra_fields_dict.items():

                        xml_element=row[key]
                        for condition in value:
                            arr.insert(condition['insert_position'],xml_element.xpath(condition['xpath_text']))

                res.append(arr)
        return header,res        
            
    def __extract_pages(self,url,paging,extra_fields_dict):
        i = 1
        res=[]
        while i < self.limit_pages:      
            page=self.__table_from_html(url+paging.format(i),extra_fields_dict={**extra_fields_dict})
            _table=page[1]
            if len(_table)==0:
                break
            else:
                _header=page[0]
                res+=_table
            i+=1  
        return _header,res
        
        
    def bonds_info(self)->dict:
        bonds_dict=self.sources['bonds']
        res={}
        for bond_group in list(bonds_dict.keys()):
            info=bonds_dict[bond_group]
            url,currency,paging=self.link+info['link'],info['currency'],info['paging']
            ticker='Тикер'
            extra_fields_dict={'Имя':[{'add_column_name':ticker
                                       ,'xpath_text':"a/@href"
                                       ,'insert_position':1
                                      } 
                                     ]}  
            if paging is None:
                res[bond_group]=(*self.__table_from_html(url,extra_fields_dict=extra_fields_dict),currency)
            else:
                 res[bond_group]=(*self.__extract_pages(url,paging,extra_fields_dict),currency)

        return res