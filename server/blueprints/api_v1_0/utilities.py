from flask import Flask, request, current_app
import subprocess, json

def obtainEnvVars():
	import json
	source1, source2 = registerSources()
	dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
	pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s && %s' %(source1,source2,dump)], stdout=subprocess.PIPE, env={})
	env_info = pipe.stdout.read()
	return json.loads(env_info)

def obtainTestEnvVars():
	import json
	source1, source2 = registerSources()
	testsrc = 'source /home/rhaeg/ros/catkin_ws/devel/setup.bash'
	dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
	pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s && %s' %(source1,testsrc,dump)], stdout=subprocess.PIPE, env={})
	env_info = pipe.stdout.read()
	return json.loads(env_info)

def registerSources():
	source1 = current_app.config["ROS_GLOBAL_SOURCE"]
	source2 = current_app.config["ROS_LOCAL_SOURCE"]
	return (source1,source2)

def parseIdParameter():
	from flask_restful import reqparse
	parser = reqparse.RequestParser()
	parser.add_argument('id')
	args = parser.parse_args()
	return args.id

def getRequestParameters():
	from flask_restful import reqparse
	parser = reqparse.RequestParser()
	args = parser.parse_args()
	print args
	return args