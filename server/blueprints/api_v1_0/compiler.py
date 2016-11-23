import gevent
# import gevent.monkey
# from gevent.pywsgi import WSGIServer
# gevent.monkey.patch_all()
from gevent.queue import Queue

from flask import jsonify, current_app, Response
from flask_restful import Resource
from flask_cors import cross_origin
from . import rest_api
from utilities import obtainEnvVars, getRunningNodes
import subprocess,os
import json


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
		# retu = []
		os.chdir(current_app.config["CATKIN_PATH"])
		pipe = executeCatkin()
		tmplist=[]
		for line in iter(pipe.stdout.readline,''):
			tmplist.append(line)
		def events():
			print(tmplist)
			q = Queue()
			for l in tmplist:
				q.put(l)
			subscriptions.append(q)
			try:
				while True:
					result = q.get()
					ev = ServerSentEvent(str(result))
					yield ev.encode()
			except GeneratorExit: # Or maybe use flask signals
				subscriptions.remove(q)
				print("---------------------failed-------------------")
				# for line in iter(pipe.stdout.readline,''):
				# 	ev = ServerSentEvent(str(result))
				# 	yield "data: %s \n\n" % (line)
				# 	gevent.sleep(1)
		return Response(events(), content_type='text/event-stream')

class debug(Resource):

	decorators = [cross_origin()]

	def get(self):
	debug_template = """
	 <html>
	   <head>
	   </head>
	   <body>
		 <h1>Server sent events</h1>
		 <div id="event"></div>
		 <script type="text/javascript">

		 var eventOutputContainer = document.getElementById("event");
		 var evtSrc = new EventSource("/subscribe");

		 evtSrc.onmessage = function(e) {
			 console.log(e.data);
			 eventOutputContainer.innerHTML = e.data;
		 };

		 </script>
	   </body>
	 </html>
	"""
	return(debug_template)


# class Catkin(Resource):

# 	decorators = [cross_origin()]

# 	def get(self):
# 		retu = [1,2,3,4,5,6,7,8,9,10]
		
# 		response.headers['content-type'] = 'text/event-stream'
# 		response.headers['Access-Control-Allow-Origin'] = '*'

# 		for line in iter(pipe.stdout.readline,''):
# 			yield "data: %s \n\n" % (line)
#  			gevent.sleep(1)

# 	def options():
# 		response.headers.update({
# 			'Access-Control-Allow-Origin': '*',
# 			'Access-Control-Allow-Methods': 'GET, OPTIONS',
# 			'Access-Control-Allow-Headers': 'X-REQUESTED-WITH, CACHE-CONTROL, LAST-EVENT-ID',
# 			'Content-Type': 'text/plain'
# 		})
# 		return ''

def executeCatkin():
	return subprocess.Popen(['catkin_make', '--force-cmake'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainEnvVars())

class ServerSentEvent(object):

	def __init__(self, data):
		self.data = data
		self.event = None
		self.id = None
		self.desc_map = {
			self.data : "data",
			self.event : "event",
			self.id : "id"
		}
	subscriptions = []
	def encode(self):
		if not self.data:
			return ""
		lines = ["%s: %s" % (v, k) 
				 for k, v in self.desc_map.iteritems() if k]
		
		return "%s\n\n" % "\n".join(lines)

rest_api.add_resource(Compile, '/compile')
rest_api.add_resource(Catkin, '/catkin')
rest_api.add_resource(RunNode, '/run')
rest_api.add_resource(GetEnvironment, '/env')
rest_api.add_resource(debug, '/debug')
rest_api.add_resource(is_running, '/is_running')
