from flask import Flask, render_template
from . import rest_api, api

@api.route('/')
def index():
	return "Root of virtual Robot"