from flask import Blueprint
api_bp= Blueprint("api_bp", __name__, template_folder='../templates')
from . import api
