from flask import Flask, request
from flask_restful import Resource
import os, subprocess
from flask_cors import cross_origin
from flask import jsonify
from . import rest_api, api

class Roscore(Resource):

	decorators = [cross_origin()]

	def get(self):
		return jsonify({'response': 'get roscore ok'})
	def post(self):
		return jsonify({'response': 'post roscore ok'})
	def put(self):
		return jsonify({'response': 'put roscore ok'})


class GetCoreAddress(Resource):

	decorators = [cross_origin()]

	def get(self):
		return jsonify({'response': 'GET response for get core address is undefined'})
	def post(self):
		json_data = request.get_json(force=True)
		print ("received core is active on" + json_data["coreAddress"])
		return "ok"


rest_api.add_resource(GetCoreAddress, '/getCoreAddress')
rest_api.add_resource(Roscore, '/roscore')