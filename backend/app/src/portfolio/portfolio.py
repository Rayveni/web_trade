from flask import render_template,request,redirect,url_for,send_file
#from datetime import datetime
from . import portfolio_bp
from os import path,getcwd
#from .config_manager import config_manager
from ..commons import flash_complex_result,exception,init_db_manager
from  pandas import read_csv

current_dir=getcwd()
template_path= path.join(current_dir,"template_stocks1.csv")


@portfolio_bp.route("/portfolio_stocks")
def portfolio_stocks():
    data={'title':'Portfolio|stocks'}



    data['optional_css_top']=['handsontable.full.min']	
    data['optional_js_bottom']=[
                                'vendor/handsontable/handsontable.full.min',
                                'js/ajax_get_data',
                                'js/bonds'] 
    return render_template('portfolio_stocks.html',data=data)
	
@portfolio_bp.route('/portfolio_stocks/action/<action_type>', methods=['GET', 'POST'])
def btn_actions(action_type):
    if action_type=="template":
        return __download_template()
    elif action_type=="upload_stocks":
        err,res=__upload_stocks(request.files['file'])
        flash_complex_result(err,res,'Executed successfully')         
        return redirect(url_for('portfolio_bp.portfolio_stocks'))
    else:
        return __download_stocks()

def __download_template():
    return send_file(template_path, as_attachment=True)

def __download_stocks():
    return 'download_stocks'
    
@exception    
def __upload_stocks(file):
    print(read_csv(file,sep=";",encoding='cp1251').columns)  
       
    return (True,None)