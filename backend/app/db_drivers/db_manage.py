from .mongo_driver import MongoDriver
from datetime import datetime

class mongo_manager(MongoDriver):
    def __convert_to_doc(self,obj,sys_date):
        res={key:getattr(obj, key) for key in obj.__slots__}
        res['sys_updated']=sys_date
        return res

    def insert_into_table_from_attr(self,table_name:str,data_attr,bulk:bool=False,update_criteria=None,rewrite=False)->tuple:
        sys_dt=datetime.now()
        if bulk:
            data=[self.__convert_to_doc(row,sys_dt) for row in data_attr]
        else:
            data=self.__convert_to_doc(data_attr,sys_dt)
        return self.insert_into_table(table_name,data,bulk,update_criteria,rewrite),sys_dt

    def __cursor_to_result(self,cursor,result='json',dict_key=None,expand_col:str=None):
        if result=='matrix':
            res=[]
            for row in cursor:
                if expand_col is not None:
                    expand_c=row.pop(expand_col)
                    row={**expand_c,**row}	                   
                res.append(list(row.values()))
            return [list(row.keys())]+res 
        elif result=='dict':
            res_d={}
            for row in cursor: 
                if expand_col is not None:
                    expand_c=row.pop(expand_col)
                    row={**expand_c,**row}                
                
                value=row.pop(dict_key)
                     
                res_d[value]=row              
            return res_d 
        else:
            res=[]            
            for row in cursor:
                if expand_col is not None:
                    expand_c=row.pop(expand_col)
                    row={**expand_c,**row} 
                res.append(row)
             
        return res
        
    def get_table(self,table_name,result='json',dict_key=None,query:dict={},columns:list=None):
        return self.__cursor_to_result(self.get_table_cursor(table_name,query=query,columns=columns,condition={'_id': False}),result,dict_key)

    def agg(self,table_name,agg_functions_list,group:list=None,sort_by=None,result='json',dict_key=None):
        """ agg_functions_list=[(func,apply_column,agg_column_name)]
         from bson.son import SON
        >>> pipeline = [
        ...     {"$unwind": "$tags"},
        ...     {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        ...     {"$sort": SON([("count", -1), ("_id", -1)])}
        ... ]

        """
        return self.__cursor_to_result(self.agg_cursor(table_name,agg_functions_list,group,sort_by),result,dict_key,expand_col='_id')

    def __convert_size(self,size_bytes:float,round_ndigits:int=2)->str:
        size_name = ("B", "KB", "MB", "GB")
        _step=1024
        prev_res=size_bytes
        for i in range(len(size_name)):
            size_bytes=size_bytes/_step
            if size_bytes<1:
                break
            prev_res=size_bytes
        return f'{round(prev_res,round_ndigits)}{size_name[i]}'

    def dbstats(self):
        _stats=self._dbstats()
        res={}
        for key,value in _stats.items():
            if str(key)[-4:]=='Size':
                res[key]=self.__convert_size(value,1)
            else:
                res[key]=value
        return res