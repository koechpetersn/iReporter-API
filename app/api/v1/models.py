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

		for item in items:
			if type(incidentType) != str or type(location) != str or type(comment) != str:
				return "invalid data"
		self.store.append(items)
		return items

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
		return "nomatch"
	def edit(self, incident_id):
		for incident in incidents:
			if incident["id"] == incident_id:
				items = request.get_json(force=True)
				for item in items:
					newval = items["location"]
					newval2 = items["comment"]
					newval3 = items["incidentType"]
					newval4 = items["media"]
				if type(newval) != str or type(newval2) != str or type(newval3) != str:
					return "invalid data"
				incident["location"] = newval
				incident["comment"] = newval2
				incident["incidentType"] = newval3
				incident["media"] = newval4
				return incident