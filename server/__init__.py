# server/__init__.py
from flask import Flask
from config import config
from flask_cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy


cors = CORS(resources={r"/": {"origins": "*"}})

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    cors.init_app(app)

    from . import models

    from blueprints.api_v1_0 import api as api_bp
    app.register_blueprint(api_bp)

    return app
