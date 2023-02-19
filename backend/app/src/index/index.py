from flask import render_template
from . import index_bp
#from backend import engine,assets_management
#from json import load,dump,dumps

#config_path='config.json'
@index_bp.route("/")
def index():
    data={'title':'index'}
    data['optional_css_top']=[#'d3_chart',
                              'handsontable.full.min']
    data['optional_js_bottom']=[#'vendor/d3/d3.v5.min',
                                'js/ajax_get_data',
                                #'vendor/crossfilter/crossfilter.min',
                                'vendor/handsontable/handsontable.full.min',
                                'js/gen_table',
                                'js/index']

    return render_template('index.html',data=data)	