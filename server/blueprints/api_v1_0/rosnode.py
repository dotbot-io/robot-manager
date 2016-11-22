from flask import Flask, request
from flask_restful import Resource
from flask_cors import cross_origin
from flask import jsonify
from . import rest_api, api
from utilities import getRunningNodes
import subprocess

class Rosnode(Resource):

	decorators = [cross_origin()]

	def get(self):
		return jsonify ({'response': 'GET request for ros node is not defined'})
	def post(self):
		json_data = request.get_json(force=True)
		node = json_data["node"]
		files = json_data["files"]
		return jsonify({'response': 'node uploaded ok'})
	def put(self):
		return jsonify({'response': 'ok'})

class RosKill(Resource):

	decorators = [cross_origin()]

	def get(self):
		return jsonify ({'response': 'GET request for kill ros node is not defined'})
	def post(self):
		json_data = request.get_json(force=True)
		print ("killing Node " +str(json_data["nodeId"]))
		return jsonify({'response': 'killed ok'})


rest_api.add_resource(RosKill, '/roskill')
rest_api.add_resource(Rosnode, '/ros_add_node')