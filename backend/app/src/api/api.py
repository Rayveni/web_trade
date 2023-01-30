from flask import jsonify,request
from . import api_bp
from app.commons import init_db_manager
from app.jobs import *


db_mng=init_db_manager()

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

