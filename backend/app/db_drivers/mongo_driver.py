from pymongo import MongoClient,DESCENDING,ASCENDING
from pandas import DataFrame
from bson.son import SON

class MongoDriver:
    __slots__ ='config','__client','db'
    def __init__(self,config: dict): 
        self.config=config    
        self.__client=MongoClient(self.config['db_url'])
        self.db=self.__client[self.config['db_name']]

    def drop_db(self):
        self.__client.drop_database(self.db.name)
		
    def drop_table(self,table):
        self.db[table].drop()		

		
    def _dbstats(self)->dict:
        return self.db.command("dbstats")
		
    def all_tables(self)->list:
        return [collection for collection in self.db.collection_names()]
 
    def table_exists(self,col_name)->bool:
        return col_name in self.all_tables()
      
    def create_table(self,table_def=None):
        pass
 
    def get_table_cursor(self,table,condition:dict={'_id': False},query:dict={},columns:list=None):
        if columns is not None:
            for field in columns:
                condition[field]=1				
        return self.db[table].find(query,condition)
		
    def agg_cursor(self,table_name,agg_functions_list,group:list=None,sort_by=None):
        """ agg_functions_list=[(func,apply_column,agg_column_name)]
         from bson.son import SON
        >>> pipeline = [
        ...     {"$unwind": "$tags"},
        ...     {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        ...     {"$sort": SON([("count", -1), ("_id", -1)])}
        ... ]

        """
        collection=self.db[table_name]
        
        if group is None:
            group=['all']
        group=list(map(str,group))
        grouper={el:'$'+el for el in group}
        agg_pipe={"_id": grouper}
        
        for el in agg_functions_list:
            func,apply_column,agg_column_name=el
            if func=='count':
                agg_pipe[agg_column_name]={"$sum": 1}
            elif func=='sum':
                 agg_pipe[agg_column_name]= {"$sum": "${}".format(apply_column)}
            else:
                pass

        pipeline=[{"$group": agg_pipe}]
        #print(pipeline)
        if sort_by:
            pipeline=	pipeline+[{"$sort": SON([el for el in sort_by])}]

        return collection.aggregate(pipeline)
			
    def merge_cursor(self,col_left,col_right,left_on,right_on,left_columns=None,right_columns=None,unwind=False,how='left',match_condition=None):
        col_l=self.db[col_left]
        filter_fields={"_join._id": 0,"_id":0}
        
        if left_columns is not None:
            #solution for exclude/include problem
            col_exclude=list(self._collection_keys(col_left)-set(left_columns)-set(['_id']))
            for field in col_exclude:
                filter_fields[field]=0    
                
        if right_columns is not None:
            col_exclude=list(self._collection_keys(col_right)-set(right_columns)-set(['_id']))            
            for field in col_exclude:
                filter_fields[f"_join.{field}"]=0                 
                
        pipeline=[{"$lookup": 
                   {'from': col_right,
                    'localField': left_on,
                    'foreignField': right_on,
                    'as': "_join"}
                  },
                  { "$project":filter_fields}
                 ]        
        if  unwind:
            pipeline.append({'$unwind':'$_join'})
        if  match_condition:
            pipeline=[{"$match":match_condition}]+pipeline
        return col_l.aggregate(pipeline)    

    def find_one(self,table,query={},return_fields=None,condition={'_id': False}):
        col=self.db[table]      
        if return_fields is not None:
            for field in return_fields:
                condition[field]=1                
        return col.find_one(query,condition)		

    def _collection_keys(self,table):
        col=self.db[table]  
        return set(col.find_one().keys())		

    def insert_into_table(self,table_name:str,data,bulk:bool=False,update_criteria=None,rewrite=False):
        collection=self.db[table_name]  
        if rewrite:
            collection.remove({})
        #sys_now=datetime.datetime.now() 
        if bulk:
            #data=[self.convert_to_doc(row,sys_now) for row in data]
            if update_criteria is None:
                return_message=collection.insert_many(data)
            else:
                return_message=collection.update_many(update_criteria, { "$set": data },upsert=True)
        else:
            #data=self.convert_to_doc(data,sys_now)
            if update_criteria is None:
                return_message=collection.insert_one(data)
            else:
                return_message=collection.update_one(update_criteria, { "$set": data },upsert=True)
        return return_message
