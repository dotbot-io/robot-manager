from flask import Flask
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask import jsonify

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/": {"origins": "*"}})

ROBOT_NAME = "macbook"
ROS_VERSION = "jade"

class Robot(Resource):

    @cross_origin(origin="*", headers=["content-type", "autorization"])
    def get(self):
        return jsonify({'name': ROBOT_NAME,
        'ros': ROS_VERSION,
        'hardware': 'macbook',
        'ros_packages': ['rosserial', 'rosbridge']})

class Roscore(Resource):

    decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]

    def get(self):
        return jsonify({'response': 'ok'})
    def post(self):
        return jsonify({'response': 'ok'})
    def put(self):
        return jsonify({'response': 'ok'})

api.add_resource(Robot, '/discovery')
api.add_resource(Roscore, '/roscore')

@app.route('/')
def index():
    return "Hello"

@app.route('/old_discovery')
@cross_origin(origin="*", headers=["content-type", "autorization"])
def disc():
    return jsonify({'name': ROBOT_NAME, 'ros': ROS_VERSION, 'hardware': 'macbook', 'ros_packages': ['rosserial', 'rosbridge']})



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
