from flask_restful import Resource
from flask import jsonify, make_response, request, abort
from app.v1.models import IncidentModel, incidents
import re
class IncidentsResource(Resource, IncidentModel):
	"""class for handling incidents"""
	def __init__(self):
		"""initialize class Resource"""
		self.store = IncidentModel()
	def post(self):
		"""Create incidents using POST method"""
		items = request.get_json(force=True)
		if "comment" not in items or "location" not in items:
			return make_response(jsonify({
				"message": "Missing fields, Please supply data for all fields"}), 201)
		if "incidentType" not in items or "media" not in items:
			return make_response(jsonify({
				"message": "Missing fields, Please supply data for all fields"}), 201)

		incidentType = items["incidentType"]
		location = items["location"]
		comment = items["comment"]
		media = items["media"]

		resp = self.validate_numbers_only(comment,location)
		if resp == "num only":
			return make_response(jsonify({
				"message": "Please provide a more comprehensive report"
				}),201)

		
		resp = self.check_whitespace(comment,location)
		if resp == "white space field":
			return make_response(jsonify({
				"message": "Missing fields, Cannot be empty"
				}),201)


		resp = self.validate_fields(incidentType, location,comment)
		if resp == "null fields":
			return make_response(jsonify({
				"message": "Missing fields, Please supply data for all fields"
				}),201)

		resp = self.validate_incidentType(incidentType)
		if resp == "invalid field data":
			return make_response(jsonify({
				"message": "Only redflag or intervention is accepted to incidentType field"
				}),201)

		resp = self.validate_mediaType(media)
		if resp == "invalid media data":
			return make_response(jsonify({
				"message": "Only image or video is accepted to media field"
				}),201)

		resp = self.check_comment(comment)
		if resp == "err":
			return make_response(jsonify({"message": "Special characters not allowed!"}),201)

		resp = self.check_location(location)
		if resp == "err":
			return make_response(jsonify({"message": "Special characters not allowed!"}),201)

		resp = self.check_type(comment,location)
		if resp == "invalid data":
			return make_response(jsonify({
				"message": "Invalid data, Please enter correct details"
				}),201)

		resp = self.store.save_incident(incidentType, location, comment, media)
		return make_response(jsonify({
			"message" : "Incident successfully captured",
			"incident" : resp
			}),201)

	def get(self):
		"""View incidents using get method"""
		resp = self.store.view_incidents() 
		if resp:
			return make_response(jsonify({
			"message": "All incidents available",
			"All incidents" : resp
			}),200) 
		return make_response(jsonify({"message" : "No incidents found"}),200)
		

class IncidentResource(Resource, IncidentModel):
	"""class for handling single incident"""
	def __init__(self):
		"""initialize Incident resource class"""
		self.store = IncidentModel()

	def get(self, incident_id):
		"""view a single specific record by id"""
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
		"""delete a specific record by id"""
		resp = self.store.remove_incident(incident_id)
		if resp == "no match":
			return make_response(jsonify({
				"message" : "No incident with that id is available for deletion!"
				}), 200)
		return make_response(jsonify({"message" : "Record deleted successfully"}), 200)
		
	def patch(self, incident_id=None):
		"""edit specific record by id"""
		for item in incidents:
			if item["id"] == incident_id:
				resp = self.store.edit(incident_id)
				success_message = "Record updated successfully"
				if resp != "invalid data":
					return make_response(jsonify({
						"message": success_message,"data":resp
						}), 200)
				
				return make_response(jsonify({
					"message":"Please ensure you supply valid data"
					}), 200)

		return make_response(jsonify({
			"message":"Really? That incident isn't available!"
			}), 200)
