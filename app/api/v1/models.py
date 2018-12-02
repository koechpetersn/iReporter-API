from flask import request
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
		if len(incidents) == 0:
			self.id = 1
		else:
			self.id = incidents[-1]['id'] + 1
		
	'''class to be inherited by all other models'''
	def save_incident(self,incidentType,location,comment):
	
		item = {
		"id": self.id,
		#"createdOn": datetime,
		#"createdBy" : self.createdBy,
		"incidentType" : incidentType,
		"location" : location,
		"status" : self.status,
		#"Images" : [Image,Image],
		#"Videos" : [Image,Image],
		"comment" : comment
		
		}
		self.store.append(item)
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