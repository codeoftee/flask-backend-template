import logging
import os
from logging.handlers import RotatingFileHandler

import pymysql
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

cors = CORS(resources={r"/v1/*": {"origins": "*"}}, supports_credentials=True)  # enable CORS for all routes
db = SQLAlchemy()
migrate = Migrate()
pymysql.install_as_MySQLdb()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    cors.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db=db)
    mail.init_app(app)

    # init blueprints
    from users import user_bp as user_blueprint
    from admin import admin_ as admin_blueprint

    app.register_blueprint(admin_blueprint, url_prefix='/v1/admin')
    app.register_blueprint(user_blueprint, url_prefix='/v1/users')

    # log to files
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/oh.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    return app
