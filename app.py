from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

ROBOT_NAME = "macbook"
ROS_VERSION = "jade"

class Robot(Resource):
    def get(self):
        return {'name': ROBOT_NAME, 'ros': ROS_VERSION}

api.add_resource(Robot, '/discovery')

@app.route('/')
def index():
    return "Hello"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
