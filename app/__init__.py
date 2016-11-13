from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/": {"origins": "*"}})

from app import views

