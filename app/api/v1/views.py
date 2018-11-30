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

	def get(self, incident_id=None):
		if incident_id:
			for item in incidents:
				if item["id"] == incident_id:
					resp = self.store.view_incident(incident_id)
					return make_response(jsonify({
						"message" : "This is your incident",
						"incident" : resp
						}),200)
	
		resp = self.store.view_incidents() 
		if resp:
			return make_response(jsonify({
			"message": "Here are your incidents",
			"All incidents" : resp
			}),200) 
		return make_response(jsonify({"message" : "No incidents found"}),404)
		

class IncidentResource(Resource):
	def __init__(self):
		self.store = IncidentModel()

	def delete(self, incident_id=None):
		for item in incidents:
			if item["id"] == incident_id:
				resp = self.store.rm()
		return  make_response(jsonify({
			"message": "delete successful",
			"All other incidents" : resp
			}),200)
