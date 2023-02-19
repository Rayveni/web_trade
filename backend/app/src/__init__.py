from flask import Flask

from .api import api_bp
from .admin import admin_bp
#from .upload_data import upload_data_bp
from .index import index_bp
from .upload import upload_bp
from .advisor import advisor_bp
from .reports import reports_bp
from .portfolio import portfolio_bp
app = Flask(__name__)
app.secret_key = 'random string'
app.static_folder = 'static'
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)
#app.register_blueprint(upload_data_bp)
app.register_blueprint(index_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(advisor_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(portfolio_bp)
