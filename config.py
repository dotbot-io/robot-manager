import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SQLALCHEMY_COMMIT_ON_TEARDOWN = 'True'
    SQLALCHEMY_ECHO=False
    SQLALCHEMY_TRACK_MODIFICATIONS=True

    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY','\xfb\x13\xdf\xa1@i\xd6>V\xc0\xbf\x8fp\x16#Z\x0b\x81\xeb\x16')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))


    @staticmethod
    def init_app(app):
        pass


class MacLudoConfig(Config):
    ROS_GLOBAL_SOURCE = 'source /opt/ros/jade/setup.bash'
    ROS_LOCAL_SOURCE = 'source /Users/ludus/develop/dotbot_ws/ros/devel/setup.bash'
    CATKIN_PATH = "/Users/ludus/develop/dotbot_ws/ros/"

class VagrantConfig(Config):
    ROS_GLOBAL_SOURCE = 'source /opt/ros/kinetic/setup.bash'
    ROS_LOCAL_SOURCE = 'source /home/vagrant/ros/dotbot_ws/devel/setup.bash'
    CATKIN_PATH = "/home/vagrant/ros/dotbot_ws/"

config = {
    'vagrant': VagrantConfig,
    'macludo': MacLudoConfig,
    'default': VagrantConfig
}
