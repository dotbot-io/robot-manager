from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/": {"origins": "*"}})

app.config.from_object('config')

from app.compiler import compiler_bp
app.register_blueprint(compiler_bp)

from app import views
from . import compiler