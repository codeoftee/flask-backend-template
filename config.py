import os
import pathlib
from datetime import timedelta


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///myapp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_FOLDER = os.path.join(pathlib.Path().absolute(), 'static/uploads')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=31)
    HOOKS_LOGS_DIR = os.path.join(pathlib.Path().absolute(), 'web/hooks')
