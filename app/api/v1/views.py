from flask_restful import Resource
from flask import jsonify, make_response, request, abort
from app.api.v1.models import IncidentModel, incidents

class IncidentsResource(Resource, IncidentModel):
	"""class for handling incidents"""
	def __init__(self):
		self.store = IncidentModel()


	
	def post(self):
		items = request.get_json(force=True)
		

		incidentType = items["incidentType"]
		location = items["location"]
		comment = items["comment"]
		media = items["media"]

		resp = self.validate_fields(incidentType, location,comment)
		if resp == "null fields":
			return make_response(jsonify({
				"msg": "Missing fields, Please supply data for all fields"
				}),201)

		resp = self.validate_incidentType(incidentType)
		if resp == "invalid field data":
			return make_response(jsonify({
				"msg": "Only redflag or intervention is accepted to incidentType field"
				}),201)

		resp = self.validate_mediaType(media)
		if resp == "invalid media data":
			return make_response(jsonify({
				"msg": "Only image or video is accepted to media field"
				}),201)

		resp = self.check_comment(comment)
		if resp == "err":
			return make_response(jsonify({"msg": "Special characters not allowed!"}),201)

		resp = self.check_location(location)
		if resp == "err":
			return make_response(jsonify({"msg": "Special characters not allowed!"}),201)

		resp = self.check_type(comment,location)
		if resp == "invalid data":
			return make_response(jsonify({
				"msg": "Invalid data, Please enter correct details"
				}),201)

		resp = self.store.save_incident(incidentType, location, comment, media)
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
		return make_response(jsonify({
			"message" : "No incident found with that id"
			}),200)

	def delete(self, incident_id):
		resp = self.store.remove_incident(incident_id)
		if resp == "no match":
			return make_response(jsonify({
				"message" : "No incident with that id is available for deletion!"
				}), 200)
		return make_response(jsonify({"message" : "Record deleted successfully"}), 200)
		


	def patch(self, incident_id=None):
		for item in incidents:
			if item["id"] == incident_id:
				resp = self.store.edit(incident_id)
				success_message = "Record updated successfully"
				if resp != "invalid data":
					return make_response(jsonify({
						"message": success_message,"data":resp
						}), 200)
				
				return make_response(jsonify({
					"error":"Please ensure you supply valid data"
					}), 200)

		return make_response(jsonify({
			"status": 200,"error": "Really? That incident isn't available!"
			}), 200)


