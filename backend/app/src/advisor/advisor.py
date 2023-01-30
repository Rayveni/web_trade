from flask import render_template,request,redirect,url_for
from datetime import datetime
from . import advisor_bp

#from .config_manager import config_manager
from app.commons import flash_complex_result,exception,init_db_manager


@exception
def __last_updated_bonds()->tuple:
    _last_upd_date=init_db_manager().find_one('upload_info',
                                              {"sys_name": "smartlabbondsusd"},
                                              return_fields=['sys_updated'])['sys_updated']
    d_diff=(datetime.now()-_last_upd_date).days
    return _last_upd_date.strftime("%Y-%m-%d %H:%M:%S"),d_diff>0

@advisor_bp.route("/bonds")
def _bonds():
    data={'title':'Advisor|bonds'}

    err,last_updated_date_tuple=__last_updated_bonds()
    if not err[0]:
        flash_complex_result(err,last_updated_date_tuple,'')
        last_updated_date,last_updated_date_alert='error updated date','danger'
    else:
        last_updated_date=last_updated_date_tuple[0]
        if last_updated_date_tuple[1]:
            last_updated_date_alert='danger'
        else:
            last_updated_date_alert='success'

    data['optional_css_top']=['handsontable.full.min','daterangepicker']
    data['last_updated_date']=last_updated_date	
    data['last_updated_date_alert']=last_updated_date_alert		
    data['optional_js_bottom']=['vendor/daterangepicker/moment.min',
                                'vendor/crossfilter/crossfilter.min',
                                'vendor/daterangepicker/daterangepicker.min',
                                'vendor/handsontable/handsontable.full.min',
                                'js/ajax_get_data',
                                'js/bonds'] 
    return render_template('bonds.html',data=data)
	
@advisor_bp.route("/stocks")
def _bonds3():
    data={'title':'Advisor|stocks'}

    err,last_updated_date_tuple=__last_updated_bonds()
    if not err[0]:
        flash_complex_result(err,last_updated_date_tuple,'')
        last_updated_date,last_updated_date_alert='error updated date','danger'
    else:
        last_updated_date=last_updated_date_tuple[0]
        if last_updated_date_tuple[1]:
            last_updated_date_alert='danger'
        else:
            last_updated_date_alert='success'

    data['optional_css_top']=['handsontable.full.min','daterangepicker']
    data['last_updated_date']=last_updated_date	
    data['last_updated_date_alert']=last_updated_date_alert		
    data['optional_js_bottom']=['vendor/daterangepicker/moment.min',
                                'vendor/crossfilter/crossfilter.min',
                                'vendor/daterangepicker/daterangepicker.min',
                                'vendor/handsontable/handsontable.full.min',
                                'js/ajax_get_data',
                                'js/bonds'] 
    return render_template('stocks.html',data=data)
	