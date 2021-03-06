import subprocess,tempfile,os
from flask import Blueprint, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from app import app
from app import api

compiler_bp = Blueprint('compiler', __name__)
api_bp = Api(compiler_bp)

class GetEnvironment(Resource):

	decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]

	def get(self):
		return "ok"
		import json
		source1 = app.config["ROS_GLOBAL_SOURCE"]
		source2 = app.config["ROS_LOCAL_SOURCE"]
		dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
		pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s && %s' %(source1,source2,dump)], stdout=subprocess.PIPE)
		print pipe
		env_info =  pipe.stdout.read()
		print env_info
		_env = json.loads(env_info)
		if 'LS_COLORS' in _env:
			del _env['LS_COLORS']
		_env["PWD"] = app.config["CATKING_PATH"]
		return jsonify(_env)

api_bp.add_resource(GetEnvironment, '/env')