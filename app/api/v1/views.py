from flask_restful import Resource
from flask import jsonify, make_response, request, abort

from app.api.v1.models import IncidentModel
from app.api.validations import DataValidation
class IncidentsResource(Resource):
	"""class for handling incidents"""
	def post(self):
		"""Create incidents using POST method"""
		items = request.get_json(force=True)
		validate_items = DataValidation(**items)
		validation = validate_items.submit()
		if not isinstance(validation,str):
			description = validation[0]
			location = validation[1]
			incident = IncidentModel(
				description,location
				)
			incident.save_incident()
			view_rec = incident.view()
			return make_response(jsonify( {
				"message":"Incident reported successfully",
				"incident":view_rec
				}),201)
		else:
			return {"message":validation},401

	def get(self):
		"""Fetch all incidents"""
		resp = IncidentModel.get()
		if resp:
			return make_response(jsonify({
				"message":"Incidents found",
				"Incidents":resp}),200)
		return {"message":"Incidents not found"},404

class IncidentResource(Resource):
	"""class for handling single incident manipulation"""
	def get(self,incident_id):

		resp = IncidentModel.get_by(incident_id)
		print(resp)
		if resp:
			return make_response(jsonify({
				"message":"Incident found",
				"Incident":resp}),200)
		return {"message":"Incident not found"},404

	def delete(self, incident_id):
		"""delete a specific record by id"""
		incident = IncidentModel.get_by(incident_id)
		if incident:
			IncidentModel.delete(incident)
			return{"message":"Record deleted successfully"},200
		return{
			"message":"Delete unsuccessful, incident not found"
			},404

	def patch(self, incident_id):
		"""edit specific record by id"""
		incident = IncidentModel.get_by(incident_id)
		if incident:
			items = request.get_json(force=True)
			validate_items = DataValidation(**items)
			validation = validate_items.submit()
			if not isinstance(validation,str):
				description = validation[0]
				location = validation[1]
				incident['location'] = location
				incident['description'] = description
				return make_response(jsonify({
					"message":"Record updated successfully",
					"new patched record":incident}),200)
			return{"message":validation},401
		return{"message":"Record update failed. Record not found"}
		




		
