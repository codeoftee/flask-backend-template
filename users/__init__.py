from flask import Blueprint
user_bp = Blueprint('_user', __name__)
from users import routes, models
