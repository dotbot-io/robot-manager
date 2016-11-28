from flask import jsonify, current_app, Response
from flask_restful import Resource, reqparse
from flask_cors import cross_origin
from . import rest_api
from utilities import obtainEnvVars, getRunningNodes,registerSources, obtainTestEnvVars
import subprocess,os
from ...models import Node

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

class Catkin(Resource):

	decorators = [cross_origin()]

	def get(self):
		pipe = executeCatkin()
		return Response(execute_procedure(pipe), content_type='text/event-stream')

	def options(self):
		pass

class Build_Node(Resource):

	decorators = [cross_origin()]

	def post(self, id):
		print (id)
		n = Node.query.get_or_404(id)
		pipe = compile(n)
		return Response(execute_procedure(pipe), content_type='text/event-stream')

	def options(self):
		pass	

class Run_Node(Resource):

	decorators = [cross_origin()]
	
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('ider')
		args = parser.parse_args()

		#n = Node.query.get_or_404(id)
		pipe = run('beginner_tutorials', 'talker.py')
		return Response(execute_procedure(pipe), content_type='text/event-stream')

	def options(self):
		pass	

def executeCatkin():
	os.chdir(current_app.config["CATKIN_PATH"])
	return subprocess.Popen(['catkin_make', '--force-cmake'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainEnvVars())

def execute_procedure(pipe):
	while True:
		line = pipe.stdout.readline()
		if line != '':
			yield "data: %s \n\n" % (line)
		else:
			yield "data: FINISHIED \n\n"
			break

def compile(node):
	if node.catkin_initialized == True:
		pipe = subprocess.Popen(['catkin_make', 'src_' + str(node.id) + '_' + current_app.config["DOTBOT_PACKAGE_NAME"]+'_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainEnvVars())
		return pipe
	else:
		pipe = executeCatkin()
		node.catkin_initialized = True
		return pipe

def run(package, node):
	# if not is_runnning(node.id):
		# pipe = subprocess.Popen(['rosrun', current_app.config["DOTBOT_PACKAGE_NAME"], node.executable()], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainEnvVars())

	pipe = subprocess.Popen(['rosrun', package, node], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainTestEnvVars())
	return pipe

rest_api.add_resource(Catkin, '/catkin')
rest_api.add_resource(GetEnvironment, '/env')
rest_api.add_resource(is_running, '/is_running')
rest_api.add_resource(Build_Node, '/build_node')
rest_api.add_resource(Run_Node, '/run_node')
