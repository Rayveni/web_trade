from flask import jsonify,request,Response
from datetime import datetime
#from json import dumps

from . import api_bp
from app.commons import init_db_manager,background_tasks
from app.jobs import *

db_mng=init_db_manager()
default_encode,default_mimetype,default_result_form='cp1251',"Content-Type: text/csv; charset=windows-1251",'matrix'
default_time_format,default_csv_delimiter="%Y-%m-%d %H:%M:%S",';'

@api_bp.route("/api/uploads_info", methods=['GET', 'POST'])
def uploads_info():
    upload_filter=request.args.get('upload_filter')  
    if db_mng.table_exists('upload_info'):
        if upload_filter is None:
            upload_info_data=db_mng.get_table('upload_info')
        else:
            upload_info_data=db_mng.get_table('upload_info',query={ 'sys_name': { '$in': upload_filter.split(',') } })
    else:
        upload_info_data=[]
    return jsonify(upload_info_data)  

@api_bp.route('/api/query_data', methods=['GET', 'POST'])
def query_data():
    #process arguments
    _res_form=request.args.get('result')
    _table=request.args.get('table')
    _params=request.args.get('params')
    _noconvert=request.args.get('noconvert')    
    _csv=request.args.get('csv')
    post_data=request.json
    
    if post_data is None:
        post_data={}
    if _res_form is None:
        _res_form=default_result_form       
    #get data  
    #get_table(table_name,result='matrix',view_id=None,params=None,post_data={},query:dict={},dict_key=None,columns=None):
    data_kvargs={'result':_res_form,'query':{},"dict_key":None,'columns':None}
    for k,v in post_data.items():
        data_kvargs[k]=v      
    data_request=db_mng.get_table(_table,**data_kvargs)
    #prepare output 
    if  _noconvert is not None or len(data_request)==0:
        pass
    else:
        last_row=data_request[-1]
        datetime_cols=[i for i in range(len(last_row)) if isinstance(last_row[i], datetime)]     
        for i in range(1, len(data_request)):
            for col in datetime_cols:   
                data_request[i][col]=data_request[i][col].strftime(default_time_format)        

    if  _csv is not None:
        csv_data= '\n'.join([default_csv_delimiter.join(map(lambda s:'' if str(s)=='nan'  else str(s), row)) for row in data_request])   
        return Response(csv_data.encode(default_encode),
                        mimetype=default_mimetype,
                        headers={"Content-disposition":"attachment; filename={}.csv".format(_table)})
    return jsonify(data_request)

@api_bp.route('/api/queue_info', methods=['GET', 'POST'])
def queue_info():
    _registry=request.args.get('registry')
    _report=request.args.get('report')    
    bt=background_tasks()
      
    if _report =='count' or _report is None:
        if _registry is None:
            res=bt._queue.count
        else:
            res=len(bt.queue_jobs(_registry))
    return jsonify(res) 
