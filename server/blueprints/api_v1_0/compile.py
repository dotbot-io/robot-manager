from flask import jsonify, current_app, Response
from flask_restful import Resource
from flask_cors import cross_origin
from . import rest_api
from utilities import obtainEnvVars, obtainTestEnvVars, parseIdParameter
import subprocess,os
from ...models import Node
from compiler import Compiler

comp = Compiler()

class GetEnvironment(Resource):

	decorators = [cross_origin()]

	def get(self):
		env = comp.env()
		return jsonify(env)

class Catkin(Resource):

	decorators = [cross_origin()]

	def get(self):
		pipe = comp.catkin()
		return Response(comp.execute_procedure(pipe), content_type='text/event-stream')

	def options(self):
		pass

class Build_Node(Resource):

	decorators = [cross_origin()]

	def post(self, id):
		# n = Node.query.get_or_404(id)
		pipe = comp.compile(n)
		return Response(comp.execute_procedure(pipe), content_type='text/event-stream')

	def options(self):
		pass	

class Run_Node(Resource):

	decorators = [cross_origin()]
	
	def get(self):
		id = parseIdParameter()
		n = Node.query.get_or_404(id)
		if (n is not None):
			pipe = comp.run('beginner_tutorials',n)
			return Response(comp.execute_procedure(pipe), content_type='text/event-stream')
		else:
			return jsonify("Node not found")

	def options(self):
		pass

class Kill_Node(Resource):

	decorators = [cross_origin()]
	
	def get(self):
		id = parseIdParameter()
		n = Node.query.get_or_404(id)
		if (n is not None):
			pipe = comp.kill(n)
			return Response(comp.execute_procedure(pipe), content_type='text/event-stream')
		else:
			return jsonify("Node not found")

	def options(self):
		pass

class Running_Nodes(Resource):

	decorators = [cross_origin()]
	
	def get(self):
		out["Process Running"] = comp.running_proc()
		out["In Compiler"] = comp.running_nodes()
		return jsonify (out)

rest_api.add_resource(Catkin, '/catkin')
rest_api.add_resource(GetEnvironment, '/env')
rest_api.add_resource(Running_Nodes, '/running_nodes')
rest_api.add_resource(Build_Node, '/build_node')
rest_api.add_resource(Run_Node, '/run_node')
rest_api.add_resource(Kill_Node, '/kill_node')
