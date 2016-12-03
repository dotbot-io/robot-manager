from flask import Flask, request, make_response, flash, jsonify
from flask_restful import Resource, reqparse
from flask_cors import cross_origin
from flask_json import JsonError, json_response, as_json
from . import rest_api, api
from ... import db
from ...models import Node
from utilities import parseIdParameter, getRequestParameters
from sqlalchemy.exc import IntegrityError

class GetNodes(Resource):

	decorators = [cross_origin()]

	def get(self):
		nodes = Node.query.all()
		return jsonify(dict(nodes=[s.to_json() for s in nodes]))

class GetNode(Resource):

	decorators = [cross_origin()]

	def get(self):
		id = parseIdParameter()
		s = Node.query.filter_by(id=id).first()
		if s is None:
			return jsonify("Node not found")
		return jsonify(s.to_json())

class AddNode(Resource):

	decorators = [cross_origin()]

	def post(self):
		from flask_restful import reqparse
		parser = reqparse.RequestParser()
		parser.add_argument('title')
		parser.add_argument('language')
		n = Node.from_rest_args(parser.parse_args())
		db.session.add(n)
		try:
			db.session.commit()
			n.create()
		except IntegrityError:
			db.session.rollback()
			flash('Title already in Database')
			raise JsonError(error='Title already in Database')
		return jsonify({'response': 'Node Posted succesfully'})
	
	def put(self):
		n = Node.query.filter_by(id=id).first()
		if n is None:
			return jsonify("Node not found")
		db.session.add(s)
		return jsonify({'response': 'ok'})

class StatusNode(Resource):

	decorators = [cross_origin()]

	def get(self):
		id = parseIdParameter()
		try:
			n = Node.query.filter_by(id=id).first()
			if n is not None:
				return jsonify(n.to_json())
		except:
			return jsonify({"ERROR": "Database Connection Error"})
	
class StatusNodes(Resource):

	decorators = [cross_origin()]

	def get(self):
		try:
			nodes = Node.query.all()
			return jsonify(dict(nodes=[{'id': n.id,'name':n.name, 'running':is_running(n.id)} for n in nodes ]))
		except:
			return jsonify({"ERROR": "Database Connection Error"})
	
class DeleteNode(Resource):

	decorators = [cross_origin()]

	def delete(self):
		try:
			id = parseIdParameter()
			n = Node.query.filter_by(id=id).first()
			if n is not None:
				db.session.delete(n)
				db.session.commit()
				return jsonify("Deleted Node Ok")
			raise JsonError(error='node not in database')
		except:
			return jsonify("Error - Something happened")


rest_api.add_resource(GetNodes, '/get_nodes')
rest_api.add_resource(GetNode, '/get_node')
rest_api.add_resource(AddNode, '/add_node')
rest_api.add_resource(DeleteNode, '/delete_node')
rest_api.add_resource(StatusNode, '/status_node')
rest_api.add_resource(StatusNodes, '/status_nodes')