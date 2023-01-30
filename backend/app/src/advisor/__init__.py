from flask import Blueprint
advisor_bp= Blueprint("advisor_bp", __name__, template_folder='../templates')
from . import advisor
