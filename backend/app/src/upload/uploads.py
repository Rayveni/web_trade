from flask import render_template,redirect,url_for,request
from . import upload_bp

from app.commons import flash_complex_result,exception,init_db_manager
from app.jobs import *


db_mng=init_db_manager()

@exception
def __get_uploads():

    if db_mng.table_exists('upload_info'):	
        return db_mng.get_table('upload_info')
    else:
        return []
		
@upload_bp.route("/upload_jobs")
def _upload_jobs():
    data={'title':'uploads'}
    _upload_contorls={'smartlabbondsrus':{'job':'job_sl_bonds','actual_date':None,'sys_updated':None},
                      'smartlabbondsusd':{'job':'job_sl_bonds','actual_date':None,'sys_updated':None},
                      'job_world_fond_indexes':{'job':'job_yahoo','actual_date':None,'sys_updated':None}, 
                      'sec_sectors':{'job':'job_sectors','actual_date':None,'sys_updated':None},
                      'mosex_securities':{'job':'job_mosex_securities','actual_date':None,'sys_updated':None}
                     }

    err,_uploads=__get_uploads()
    if not err[0]:
        flash_complex_result(err,_uploads,'')
        _upload_dict={}
    else:
        for row in _uploads:
            _key=row['sys_name']
            try:
                _val=_upload_contorls[_key]
                _val['actual_date']=row['actual_date'].strftime("%d-%m-%Y %H:%M:%S")
                _val['sys_updated']=row['sys_updated'].strftime("%d-%m-%Y %H:%M:%S")
            except:
                _upload_contorls[_key]={'job':'None','actual_date':row['actual_date'],'sys_updated':row['sys_updated']}   
    data['upload_controls']= _upload_contorls

    return render_template('upload_jobs.html',data=data)	
	
 
@exception
def __exec_job(job_name):
    _job=eval(job_name)
    return _job(db_mng)
	
@upload_bp.route(r"/run_job/<params>", methods=['GET', 'POST'])  
def _run_job(params):
    _redirect_url=request.args.get('redirect_url')

    if params == 'None':
        flash_complex_result((False,'None parameter passed'),None,None)  
    elif params == 'all':
        break_flg=False
        for _job in ['job_sectors','job_sl_bonds','job_yahoo','job_mosex_securities']:
            err,res=__exec_job(_job)
            if err[0] is False:
                flash_complex_result(err,res,'Executed successfully')
                break_flg=True
                break
        if break_flg is False:
            flash_complex_result(err,res,'Executed successfully')        
    else:
 
        err,res=__exec_job(params)        
        flash_complex_result(err,res,'Executed successfully')
    if _redirect_url is not None:

        return redirect(url_for(_redirect_url))
    return redirect(url_for('upload_bp._upload_jobs'))



