from flask_restful import Resource
from flask import jsonify, make_response, request, abort
from app.api.v1.models import IncidentModel, incidents

class IncidentsResource(Resource, IncidentModel):
	"""class for handling incidents"""
	def __init__(self):
		self.store = IncidentModel()


	
	def post(self):
		items = request.get_json(force=True)
		fields=items.keys()
		for key in fields:
			if not items[key]:
				return make_response(jsonify({"msg": "Missing fields, Please supply data for all fields"}),201)

		incidentType = items["incidentType"]
		location = items["location"]
		comment = items["comment"]
		media = items["media"]


		resp = self.store.save_incident(incidentType, location, comment, media)
		if resp == "invalid data":
			return make_response(jsonify({"msg": "Invalid data, Please enter correct details"}),201)	
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
		return make_response(jsonify({"message" : "No incidents found"}),200)
		

class IncidentResource(Resource, IncidentModel):
	"""class for handling single incidents"""
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
		return make_response(jsonify({"message" : "No incident found with that id"}),200)

	def delete(self, incident_id):
		resp = self.store.remove_incident(incident_id)
		if resp == "nomatch":
			return make_response(jsonify({"message" : "No incident with that id is available for deletion!"}), 200)
		return make_response(jsonify({"message" : "Record deleted successfully"}), 200)
		


	def patch(self, incident_id=None):
		for item in incidents:
			if item["id"] == incident_id:
				resp = self.store.edit(incident_id)
				success_message = "Record updated successfully"
				if resp != "invalid data":
					return make_response(jsonify({"message": success_message,"data":resp}), 200)
				
				return make_response(jsonify({"error":resp}), 200)

		return make_response(jsonify({"status": 200,"error": "Red-flag does not exist"}), 200)


