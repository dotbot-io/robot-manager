from flask import Flask, request, make_response, jsonify, flash
from flask_restful import Resource
from flask_cors import cross_origin
from flask_json import JsonError, json_response, as_json
from . import rest_api, api
from ... import db
from ...models import File, Node
from utilities import parseIdParameter, getRequestParameters
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import os

class AddFile(Resource):

	decorators = [cross_origin()]

	def post(self):
		node_id = parseIdParameter()

		n = Node.query.filter_by(id=node_id).first()
		if n is None:
			return jsonify("Node not found")
		from flask_restful import reqparse
		parser = reqparse.RequestParser()
		parser.add_argument('filename')
		parser.add_argument('code')
		f = File.from_rest_args(parser.parse_args())
		f.node = n
		f.filename = os.path.join(n._folder(), f.filename)
		db.session.add(f)
		try:
			db.session.commit()
			f.save()
		except IntegrityError:
			db.session.rollback()
			flash('File already in Database')
			raise JsonError(error='File already in Database')
		return jsonify('File posted succesfully')
	
	def put(self):
		id = parseIdParameter()
		f = File.query.ilter_by(id=id).first()
		if f is None:
			return jsonify("Node not found")
		args = getRequestParameters()
		f.code = args.code
		f.last_edit = datetime.utcnow()
		db.session.add(f)
		f.save()
		return jsonify('File put succesfully')

class GetFiles(Resource):

	decorators = [cross_origin()]

	def get(self):
		files = File.query.all()
		return jsonify(dict(files=[f.to_json() for f in files]))

class GetNodeFiles(Resource):

	decorators = [cross_origin()]

	def get(self):
		id = parseIdParameter()
		files = File.query.filter_by(node_id=id).all()
		if len(files)==0:
			return jsonify("No Files")
		return jsonify(dict(files=[f.to_json() for f in files]))

class GetFile(Resource):

	decorators = [cross_origin()]

	def get(self):
		id = parseIdParameter()
		file = File.query.filter_by(id=id).first()
		if file is None:
			return jsonify("No File")
		return jsonify(dict(file=file.to_json()))

class DeleteFile(Resource):

	decorators = [cross_origin()]

	def delete(self):
		try:
			id = parseIdParameter()
			f = File.query.filter_by(id=id).first()
			if f is not None:
				f.delete()
				return jsonify('File deleted succesfully')
			raise JsonError(error='node not in database')
		except:
			return jsonify("Error - Something happened")

class DownloadFile(Resource):

	decorators = [cross_origin()]

	def get(self):
		id = parseIdParameter()
		f = File.query.filter_by(id=id).first()
		if f is None:
			return jsonify("Node not found")
		# n = Node.query.filter_by(id=f.node_id).first()
		response = make_response(f.code)
		response.headers["Content-Disposition"] = "attachment; filename=%s" % f.filename
		return response


rest_api.add_resource(AddFile, '/add_file')
rest_api.add_resource(GetFiles, '/get_files')
rest_api.add_resource(GetNodeFiles, '/node_files')
rest_api.add_resource(GetFile, '/get_file')
rest_api.add_resource(DeleteFile, '/delete_file')
rest_api.add_resource(DownloadFile, '/download_file')
