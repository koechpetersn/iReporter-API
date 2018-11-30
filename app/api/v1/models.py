'''Models and their methods'''
incidents = []

class IncidentModel():
	def __init__(self):
		self.store = incidents
		if len(incidents) == 0:
			self.id = 1
		else:
			self.id = incidents[-1]['id'] + 1
		
	'''class to be inherited by all other models'''
	def save_incident(self,title,nature,comment):
	
		item = {
		"id": self.id,
		"title" : title,
		"nature" : nature,
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
	def rm(self):
		for incident in incidents:
			item = incident
		self.store.remove(item)
		return self.store
		
	def edit(self, flag_id, data):
		for post in self.db:
			if post[id] == flag_id:
				post.update(data)
				return post


