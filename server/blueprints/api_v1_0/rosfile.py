from flask import Flask, request
from flask_restful import Resource
from flask_cors import cross_origin
from flask import jsonify
from . import rest_api, api

class Rosfile(Resource):

	decorators = [cross_origin()]

	def get(self):
		return jsonify ({'response': 'GET request for ros file is not defined'})
	def post(self):
		json_data = request.get_json(force=True)
		filecontent = json_data["filecontent"]
		print (filecontent)
		filename = json_data["filename"]
		print (filename)
		return jsonify({'response': 'ok'})
	def put(self):
		return jsonify({'response': 'ok'})

rest_api.add_resource(Rosfile, '/rosfile')