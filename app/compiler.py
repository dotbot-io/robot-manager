import subprocess
import tempfile
import os
from app import app
from app import api

class GetEnvironment(Resource):

	decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]

    def get(self):
        import json
        source1 = app.config("ROS_LOCAL_SOURCE")
        source2 = app.config("ROS_GLOBAL_SOURCE")
        dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
        pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s && %s' %(source1,source2,dump)], stdout=subprocess.PIPE)
        env_info =  pipe.stdout.read()
        _env = json.loads(env_info)
        if 'LS_COLORS' in _env:
            del _env['LS_COLORS']
        _env["PWD"] = app.config("CATKING_PATH")
        return jsonify(_env)

api.add_resource(GetEnvironment, '/env')