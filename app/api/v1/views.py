from flask_restful import Resource
from flask import jsonify, make_response, request, abort
from app.api.v1.models import IncidentModel, incidents

class IncidentsResource(Resource, IncidentModel):
	'''class for handling incidents'''
	def __init__(self):
		self.store = IncidentModel()


	
	def post(self):
		item = request.get_json(force=True)
		title = item["title"]
		nature = item["nature"]
		comment = item["comment"]
		resp = self.store.save_incident(title, nature, comment)
		return make_response(jsonify({
			"message" : "Incident successfully captured",
			"incident" : resp
			}),201)
