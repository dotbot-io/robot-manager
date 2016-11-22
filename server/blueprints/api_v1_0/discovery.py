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
			return jsonify({'name': envVars['USER'],
			'ros': envVars['ROS_DISTRO'],
			'hardware': envVars['SESSION_MANAGER'].split('/')[1].split(':')[0] or 'None',
			'message': 'hi, i am '+ROBOT_NAME,
			'ros_packages': ['rosserial', 'rosbridge'],
			'OS' : envVars['SESSION'] or 'Ubuntu',
			'ros_ip' : envVars['ROS_IP'] or 'None'})
		except:
			return jsonify({
				'message': 'default message, some of environment variables were not found',
				})

rest_api.add_resource(Robot, '/discovery')