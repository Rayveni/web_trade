from flask import Blueprint
index_bp= Blueprint("index_bp", __name__, template_folder='../templates')
from . import index