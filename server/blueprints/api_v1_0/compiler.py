import subprocess,tempfile,os
from flask import jsonify, current_app
from flask_restful import Resource
from flask_cors import cross_origin
from . import rest_api


class GetEnvironment(Resource):

	decorators = [cross_origin()]

	def get(self):
		import json
		source1 = current_app.config["ROS_GLOBAL_SOURCE"]
		source2 = current_app.config["ROS_LOCAL_SOURCE"]
		dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
		pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s && %s' %(source1,source2,dump)], stdout=subprocess.PIPE)
		print pipe
		env_info =  pipe.stdout.read()
		print env_info
		_env = json.loads(env_info)
		if 'LS_COLORS' in _env:
			del _env['LS_COLORS']
		_env["PWD"] = current_app.config["CATKIN_PATH"]
		return jsonify(_env)

rest_api.add_resource(GetEnvironment, '/env')
