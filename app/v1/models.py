import datetime
import re
from flask import request
'''Models and their methods'''
incidents = []
"""set incidents to an empty list"""
users = []
"""set incidents to an empty list"""
class UserModel():
	"""class to handle user models"""
	def __init__(self):
		"""Initialize class user model"""
		self.user=users
		if len(users) == 0:
			self.createdBy = 1
		else:
			self.createdBy = users[-1]["createdBy"] + 1

class IncidentModel(UserModel):
	"""class to handle incident models"""
	def __init__(self):
		"""initialize class incident model"""
		self.store = incidents
		self.status = "Draft"
		self.timenow = datetime.datetime.now()
		if len(incidents) == 0:
			self.id = 1
		else:
			self.id = incidents[-1]['id'] + 1

			
	def validate_fields(self,incidentType,location,comment):
		"""check for empty strings"""
		items = {
		"incidentType" : incidentType,
		"location" : location,
		"comment": comment
		}
		fields=items.keys()
		for key in fields:
			if not items[key]:
				return "null fields"
	def validate_numbers_only(self,comment,location):
		"""check for number input only"""
		items = {
		"location" : location,
		"comment": comment
		}
		if type(comment) == int or type(location) == int:
			return True
		if re.match(r"[0-999999]",comment) or re.match(r"[0-9999]",location):
			return "num only"
	def check_whitespace(self,location,comment):
		"""check for whitespace"""
		items = {
		"comment": comment,
		"location": location
		}
		if type(comment) == int or type(location) == int:
			return True
		resp = comment.isspace() or location.isspace()
		if resp == False:
			return True
		return "white space field"

	def validate_incidentType(self,incidentType):
		"""check for correct predetermined type of incident"""
		items = {
		"incidentType":incidentType
		}
		if items["incidentType"]=="redflag" or items["incidentType"] == "intervention":
			return True
		return "invalid field data"

	def validate_mediaType(self,media):
		"""check for correct predetermined type of media"""
		items = {
		"media" : media
		}
		if items["media"]=="image" or items["media"] == "video":
			return True
		return "invalid media data"

	def check_comment(self,comment):
		"""check for special characters"""
		items = {
		"comment": comment
		}
		if type(comment) == int:
			return True
		if not re.match(r"[A-Za-z]",comment):
			return "err"

	def check_location(self,location):
		"""check for special characters"""
		items = {
		"location": location
		}
		if type(location) == int:
			return True
		regex = re.compile(r'\A[a-zA-Z0-9*]+\Z')
		
		if not regex.match(location):
			return "err"
	def check_type(self,location,comment):
		"""check for data type"""
		items = {
		"location" : location,
		"comment" : comment
		}
		for items in items:
			if type(location) != str or type(comment) != str:
				return "invalid data"
			return True

	def save_incident(self,incidentType,location,comment,media):
		"""adding items to incidents empty list using append method"""
	
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

		self.store.append(items)
		return items

	def view_incidents(self):
		"""view all records"""
		return self.store

	def view_incident(self, incident_id):
		"""view a single specific incident by id"""
		for incident in incidents:
			if incident_id == incident["id"]:
				return incident

	def remove_incident(self,incident_id):
		"""delete an incident by id"""
		for item in incidents:
			if item["id"] == incident_id:
				new_dataset = self.store.remove(item)
				return new_dataset
		return "no match"

	def edit(self, incident_id):
		"""edit an incident by id"""
		for incident in incidents:
			if incident["id"] == incident_id:
				resp = self.validate_special_char_location()
				if resp == "invalid data":
					return "invalid data"
				items = request.get_json(force=True)
				for item in items:
					newval = items["location"]
					newval2 = items["comment"]
					newval3 = items["incidentType"]
					newval4 = items["media"]
				resp = self.validate_type()
				if resp == "invalid data":
					return "invalid data"
				incident["location"] = newval
				incident["comment"] = newval2
				incident["incidentType"] = newval3
				incident["media"] = newval4
				return incident

	def check_empty_fields(self):
		"""check for empty fields before updating data"""
		items = request.get_json(force=True)
		incidentType = items["incidentType"]
		location = items["location"]
		comment = items["comment"]
		resp = self.validate_fields(incidentType, location,comment)
		if resp == "null fields":
			return "invalid data"

	def validate_incidentType_edit(self):
		"""check for valid incident type before updating data"""
		items = request.get_json(force=True)
		incidentType = items["incidentType"]
		resp = self.validate_incidentType(incidentType)
		if resp == "invalid field data":
			return "invalid data"
		return self.check_empty_fields()

	def validate_media_edit(self):
		"""check for valid media type before updating data"""
		items = request.get_json(force=True)
		media = items["media"]
		resp = self.validate_mediaType(media)
		if resp == "invalid media data":
			return "invalid data"
		return self.validate_incidentType_edit()

	def validate_special_char_comment(self):
		"""check for special character in comment field before updating"""
		items = request.get_json(force=True)
		comment = items["comment"]
		resp = self.check_comment(comment)
		if resp == "err":
			return "invalid data"
		return self.validate_media_edit()

	def validate_special_char_location(self):
		"""check for special character in location field before updating"""
		items = request.get_json(force=True)
		location = items["location"]
		resp = self.check_location(location)
		if resp == "err":
			return "invalid data"
		return self.validate_special_char_comment()

	def validate_type(self):
		"""check for data type before updating"""
		items = request.get_json(force=True)
		newval = items["location"]
		newval2 = items["comment"]
		resp = self.check_type(newval,newval2)
		if resp == "invalid data":
			return "invalid data"
