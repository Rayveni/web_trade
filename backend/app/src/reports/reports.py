from flask import render_template,request,redirect,url_for
from datetime import datetime
from . import reports_bp

#from .config_manager import config_manager
from ..commons import flash_complex_result,exception,init_db_manager


@exception
def __last_updated_indexes()->tuple:
    _last_upd_date=init_db_manager().find_one('upload_info',
                                              {"sys_name": "job_world_fond_indexes"},
                                              return_fields=['sys_updated'])['sys_updated']
    d_diff=(datetime.now()-_last_upd_date).days
    return _last_upd_date.strftime("%Y-%m-%d %H:%M:%S"),d_diff>0

@reports_bp.route("/reports/markets")
def _bonds():
    data={'title':'Reports|markets'}

    err,last_updated_date_tuple=__last_updated_indexes()
    if not err[0]:
        flash_complex_result(err,last_updated_date_tuple,'')
        last_updated_date,last_updated_date_alert='error updated date','danger'
    else:
        last_updated_date=last_updated_date_tuple[0]
        if last_updated_date_tuple[1]:
            last_updated_date_alert='danger'
        else:
            last_updated_date_alert='success'

    data['optional_css_top']=['d3_chart']
    data['last_updated_date']=last_updated_date	
    data['last_updated_date_alert']=last_updated_date_alert		
    data['optional_js_bottom']=['vendor/d3/d3.v5.min',
                                'js/ajax_get_data',
                                'js/d3_chart',								
                                'vendor/handsontable/handsontable.full.min','js/gen_table','js/markets'] 
    return render_template('markets.html',data=data)
	
