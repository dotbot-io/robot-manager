import subprocess
import tempfile
import os
from flask import current_app
from utilities import obtainEnvVars,obtainTestEnvVars

class Compiler:

	def __init__ (self):
		self._pnodes = {}
		self._env = None
		pass

	def env(self):
		_env = obtainEnvVars()
		if 'LS_COLORS' in _env:
			del _env['LS_COLORS']
		_env["PWD"] = current_app.config["CATKIN_PATH"]
		self._env = _env
		return _env

	def run(self, package, node):
		import time
		if not self.is_runnning(node.id):
			list_before = self.running_proc()
			pipe = subprocess.Popen(['rosrun', package, node.executable()],bufsize=1 ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainTestEnvVars(),  universal_newlines=True)
			time.sleep(1)
			list_after = self.running_proc()
			diff = lambda list_before,list_after: [x for x in list_after if x not in list_before]
			new_node = diff(list_before,list_after)
			# self._pnodes[node.id] = new_node[0]
			return pipe

	def kill(self, node):
		if self.is_runnning(node.id):
			if node.id in self._pnodes.keys():
				pipe = subprocess.Popen(['rosnode', 'kill', str(self._pnodes[node.id])], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainTestEnvVars())
				del(self._pnodes[node.id])
				return pipe

	def is_runnning(self, id):
		if id in self._pnodes:
			return True
		return False

	def catkin(self):
		os.chdir(current_app.config["CATKIN_PATH"])
		return subprocess.Popen(['catkin_make', '--force-cmake'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainEnvVars())

	def execute_procedure(self, pipe):
		while True:			
			line = pipe.stdout.readline()
			if line != '':
				yield "data: %s \n\n" % (line)
			else:
				yield "data: FINISHIED \n\n"
				break	

	def compile(self, node):
		if node.catkin_initialized == True:
			pipe = subprocess.Popen(['catkin_make', 'src_' + str(node.id) + '_' + current_app.config["DOTBOT_PACKAGE_NAME"]+'_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=obtainEnvVars())
			return pipe
		else:
			pipe = catkin()
			node.catkin_initialized = True
			return pipe

	def running_nodes(self):
		return self._pnodes

	def running_proc(self):
		pipe = subprocess.Popen(['rosnode', 'list'], stdout=subprocess.PIPE)
		nodes_info = []
		while True:
			line = pipe.stdout.readline()
			if line != '':
				nodes_info.append(line.rstrip())
			else:
				break
		return nodes_info