from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_cors import cross_origin
from flask import jsonify
from . import rest_api, api
from utilities import getRunningNodes
import subprocess
import compiler

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

class StatusNode(Resource):

	decorators = [cross_origin()]

	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('id')
		args = parser.parse_args()
		try:
			n = Node.query.filter_by(id=id).first()
			if n is not None:
				return jsonify(n)
		except:
			return jsonify({"ERROR": "Database Connection Error"})
	
class StatusNodes(Resource):

	decorators = [cross_origin()]

	def get(self):
		try:
			n = Node.query.filter_by(id=id).first()
			if n is not None:
				return jsonify(dict(nodes=[{'id': n.id, 'running':compiler.is_runnning(n.id)} for n in nodes ]))
		except:
			return jsonify({"ERROR": "Database Connection Error"})

class RosKill(Resource):

	decorators = [cross_origin()]	

	def get(self):
		return jsonify ({'response': 'GET request for kill ros node is not defined'})
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('id')
		args = parser.parse_args()
		print ("killing Node " +str(args.id))
		###########
		return jsonify({'response': 'killed ok'})

rest_api.add_resource(RosKill, '/roskill')
rest_api.add_resource(Rosnode, '/ros_add_node')
rest_api.add_resource(StatusNode, '/status_node')
rest_api.add_resource(StatusNodes, '/status_nodes')