from flask import jsonify, current_app, Response
from flask_restful import Resource
from flask_cors import cross_origin
from . import rest_api
from utilities import obtainEnvVars, getRunningNodes
import subprocess,os, flask_sse
from json import dumps


class GetEnvironment(Resource):

	decorators = [cross_origin()]

	def get(self):
		_env = obtainEnvVars()
		if 'LS_COLORS' in _env:
			del _env['LS_COLORS']
		_env["PWD"] = current_app.config["CATKIN_PATH"]
		return jsonify(_env)


class is_running(Resource):

	decorators = [cross_origin()]

	def get(self):
		return "not defined"
	def post(self, id):
		runningNodes = getRunningNodes()
		if id in runningNodes:
			if runningNodes.poll() is None:
				return True
		return False

class RunNode(Resource):

	decorators = [cross_origin()]

	def get(self):
		return "not defined"
	def post(self, node):
		if not is_runnning(node.id):
			subprocess.Popen(['rosrun', current_app.config["DOTBOT_PACKAGE_NAME"], node.executable()], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainEnvVars())

class Compile(Resource):

	decorators = [cross_origin()]

	def get(self):
		return "not defined"
	def post(self, node):
		os.chdir(current_app.config["CATKIN_PATH"])
		if node.catkin_initialized == True:
			subprocess.Popen(['catkin_make', 'src_' + str(node.id) + '_' + current_app.config["DOTBOT_PACKAGE_NAME"]+'_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=self.env())
		else:
			executeCatkin()
			node.catkin_initialized = True
		return True
		# add indication for the user to know that the compilation was succesful or not

class Catkin(Resource):

	decorators = [cross_origin()]

	def get(self):
		retu = []
		os.chdir(current_app.config["CATKIN_PATH"])
		pipe = executeCatkin()
		def events():
			for line in iter(pipe.stdout.readline,''):
				yield "data: %s \n\n" % (line)
		return Response(events(), content_type='text/event-stream')

def executeCatkin():
	return subprocess.Popen(['catkin_make', '--force-cmake'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainEnvVars())

rest_api.add_resource(Compile, '/compile')
rest_api.add_resource(Catkin, '/catkin')
rest_api.add_resource(RunNode, '/run')
rest_api.add_resource(GetEnvironment, '/env')
rest_api.add_resource(is_running, '/is_running')
