#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager, Shell
from server import create_app
# from flask_migrate import Migrate, MigrateCommand
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
is_sqlite = app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:')
# migrate = Migrate(app, db, render_as_batch=is_sqlite)


@manager.command
def hello():
    print "hello"

'''
@manager.command
def deploy():

    print 'adding roles.....'
    roles = Role.query.all()
    admin = Role(name='admin')
    early = Role(name='early')
    normale = Role(name='user')

    for role in (admin, early, normale):
        if Role.query.filter_by(name=role.name).first() is None:
            print 'adding', role
            db.session.add(role)
    db.session.commit()
    print 'done'

    print 'adding admin.....'
    u = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
    if u is None:
        u = User(email=app.config['ADMIN_EMAIL'], password=app.config['ADMIN_PASSWORD'])
        db.session.add(u)
    u.password = app.config['ADMIN_PASSWORD']
    u.active = True
    admin = Role.query.filter_by(name='admin').first()
    if admin not in u.roles:
        u.roles.append(admin)
    try:
        db.session.commit()
    except:
        print 'Error: user already exist'
    print 'done'


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Sketch=Sketch)
manager.add_command("shell", Shell(make_context=make_shell_context))


manager.add_command('db', MigrateCommand)
'''


if __name__ == "__main__":
    manager.run()
