from flask import Flask, request
from flask_restful import Resource
from flask_cors import cross_origin
from flask import jsonify
from . import rest_api, api
from utilities import obtainEnvVars

ROBOT_NAME = "ubuntu_anton"
ROS_VERSION = "indigo"

class Robot(Resource):

	decorators = [cross_origin()]

	def get(self):
		envVars = obtainEnvVars()
		try:
			return jsonify({'name': envVars.get('USER',"Undefined"),
			'ros': envVars.get('ROS_DISTRO',"Undefined"),
			'message': 'hi, i am '+ROBOT_NAME,
			'ros_packages': ['rosserial', 'rosbridge'],
			'OS' : envVars.get('SESSION',"Undefined"),
			'ros_ip' : envVars.get('ROS_IP',"Undefined"),
			'test_none': envVars.get('blaaaaaaaa',"Undefined")})
		except:
			return jsonify({
				'message': 'default message, some of environment variables were not found',
				})

rest_api.add_resource(Robot, '/discovery')
