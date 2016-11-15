from flask import Blueprint
from flask_restful import Api


api = Blueprint('api_v1_0', __name__)
rest_api = Api(api)


from compiler import *
from views import *
