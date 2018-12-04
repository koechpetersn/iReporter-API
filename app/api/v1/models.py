from flask import request
import datetime
'''Models and their methods'''
incidents = []
users = []
class UserModel():
	def __init__(self):
		self.user=users
		if len(users) == 0:
			self.createdBy = 1
		else:
			self.createdBy = users[-1]["createdBy"] + 1

class IncidentModel(UserModel):
	def __init__(self):
		self.store = incidents
		self.status = "Draft"
		self.timenow = datetime.datetime.now()
		if len(incidents) == 0:
			self.id = 1
		else:
			self.id = incidents[-1]['id'] + 1
		
	def save_incident(self,incidentType,location,comment,media):
	
		items = {
		"id": self.id,
		"createdOn": self.timenow,
		"createdBy" : UserModel().createdBy,
		"incidentType" : incidentType,
		"location" : location,
		"status" : self.status,
		'media': media,
		"comment" : comment
		
		}
		msg1 = "invalid data"

		for item in items:
			if type(incidentType) != str or type(location) != str or type(comment) != str:
				return msg1 
		self.store.append(items)
		return self.store

	def view_incidents(self):
		return self.store

	def view_incident(self, incident_id):
		for incident in incidents:
			if incident_id == incident["id"]:
				return incident
	def remove_incident(self,incident_id):
		for item in incidents:
			if item["id"] == incident_id:
				new_dataset = self.store.remove(item)
				return new_dataset
		
	def edit(self, incident_id):
		for incident in incidents:
			if incident["id"] == incident_id:
				item = request.get_json(force=True)
				newval = item["location"]
				newval2 = item["comment"]
				incident["location"] = newval
				incident["comment"] = newval2
				return incident