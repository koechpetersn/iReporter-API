from flask_restful import Resource
from flask import jsonify, make_response, request, abort
from app.api.v1.models import IncidentModel, incidents

class IncidentsResource(Resource, IncidentModel):
	'''class for handling incidents'''
	def __init__(self):
		self.store = IncidentModel()


	
	def post(self):
		item = request.get_json(force=True)
		incidentType = item["incidentType"]
		location = item["location"]
		comment = item["comment"]
		resp = self.store.save_incident(incidentType, location, comment)
		return make_response(jsonify({
			"message" : "Incident successfully captured",
			"incident" : resp
			}),201)

	def get(self):
		resp = self.store.view_incidents() 
		if resp:
			return make_response(jsonify({
			"message": "All incidents available",
			"All incidents" : resp
			}),200) 
		return make_response(jsonify({"message" : "No incidents found"}),404)
		

class IncidentResource(Resource, IncidentModel):
	def __init__(self):
		self.store = IncidentModel()

	def get(self, incident_id):
		if len(incidents) >0:
			for item in incidents:
				if item["id"] == incident_id:
					resp = self.store.view_incident(incident_id)
					return make_response(jsonify({
						"message" : "Incident found!",
						"incident" : resp
						}),200)
				
		return make_response(jsonify({"message" : "No incidents found"}),404)


