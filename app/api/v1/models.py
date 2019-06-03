import datetime
from flask import request

class DB():
	"""cls"""
	def __init__(self):
		'''Create an empty database.'''

		self.incidents = []

	def drop(self):
		'''Drop entire database.'''
		self.__init__()

db = DB()

class IncidentModel():
	"""class to handle incident models"""
	
	def __init__(self,description,location):
		"""initialize class incident model"""
		self.description = description
		self.location = location
		self.tablename = 'incidents'
		if len(db.incidents) == 0:
			self.id = 1
		else:
			self.id = db.incidents[-1]['id'] + 1
		self.status = "Draft"
		self.dateCreated = datetime.datetime.now()

	def view (self):
		incident = {
			"id":self.id,
			"CreatedOn":self.dateCreated,
			"location":self.location,
			"status":self.status,
			"description":self.description
		}
		return incident

	def save_incident(self):
		"""adding items to incidents empty list using append method"""
		items = {
		"id": self.id,
		"createdOn": self.dateCreated,
		"location" : self.location,
		"status" : self.status,
		"description" : self.description
		}
		getattr(db, self.tablename).append(items)

	@classmethod
	def get(cls):
		"""get all records"""
		return db.incidents

	@staticmethod
	def get_by(incident_id):
		"""def"""
		for item in db.incidents:
			if item['id']==incident_id:
				return item
		return None
	@staticmethod
	def delete(incident):
		"""del"""
		db.incidents.remove(incident)

			
