from flask import Blueprint
admin_ = Blueprint('admin_', __name__)
from admin import routes
