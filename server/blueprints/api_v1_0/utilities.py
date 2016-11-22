from flask import Flask, request, current_app
import subprocess

def obtainEnvVars():
	import json
	source1, source2 = registerSources()
	dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
	pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s && %s' %(source1,source2,dump)], stdout=subprocess.PIPE)
	env_info = pipe.stdout.read()
	return json.loads(env_info)

def registerSources():
	source1 = current_app.config["ROS_GLOBAL_SOURCE"]
	source2 = current_app.config["ROS_LOCAL_SOURCE"]
	return (source1,source2)

def getRunningNodes():
	source1, source2 = registerSources()
	pipe = subprocess.Popen(['rosnode', 'list'], stdout=subprocess.PIPE)
	return pipe.stdout.read()
