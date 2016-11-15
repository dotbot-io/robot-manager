from flask import Flask, request
from flask_restful import Resource
import os, subprocess
from flask_cors import cross_origin
from flask import jsonify
from . import rest_api, api

ROBOT_NAME = "macbook"
ROS_VERSION = "jade"

class Robot(Resource):

	@cross_origin(origin="*", headers=["content-type", "autorization"])
	def get(self):
		return jsonify({'name': ROBOT_NAME,
		'ros': ROS_VERSION,
		'hardware': 'macbook',
		'message': 'hi, i am '+ROBOT_NAME,
		'ros_packages': ['rosserial', 'rosbridge']})

class Roscore(Resource):

	decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]

	def get(self):
		return jsonify({'response': 'get roscore ok'})
	def post(self):
		return jsonify({'response': 'post roscore ok'})
	def put(self):
		return jsonify({'response': 'put roscore ok'})

class Rosfile(Resource):

	decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]

	def post(self):
		json_data = request.get_json(force=True)
		filecontent = json_data["filecontent"]
		print (filecontent)
		filename = json_data["filename"]
		print (filename)
		return jsonify({'response': 'ok'})
	def put(self):
		return jsonify({'response': 'ok'})

class Rosnode(Resource):

	decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]

	def post(self):
		json_data = request.get_json(force=True)
		node = json_data["node"]
		files = json_data["files"]
		print(node)
		print (files)
		return jsonify({'response': 'node uploaded ok'})
	def put(self):
		return jsonify({'response': 'ok'})

class RosKill(Resource):

	decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]

	def post(self):
		json_data = request.get_json(force=True)
		print ("killing Node " +str(json_data["nodeId"]))
		return jsonify({'response': 'killed ok'})

class GetCoreAddress(Resource):

	decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]

	def post(self):
		json_data = request.get_json(force=True)
		print ("received core is active on" + json_data["coreAddress"])
		return "ok"

rest_api.add_resource(GetCoreAddress, '/getCoreAddress')
rest_api.add_resource(RosKill, '/roskill')
rest_api.add_resource(Rosnode, '/rosnode')
rest_api.add_resource(Rosfile, '/rosfile')
rest_api.add_resource(Robot, '/discovery')
rest_api.add_resource(Roscore, '/roscore')

@api.route('/')
def index():
	return "Hello"
