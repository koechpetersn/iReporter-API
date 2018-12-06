from flask import request
import datetime
import re
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
			
	def validate_fields(self,incidentType,location,comment):
		items = {
		"incidentType" : incidentType,
		"location" : location,
		"comment": comment
		}
		fields=items.keys()
		for key in fields:
			if not items[key]:
				return "null fields"

	def validate_incidentType(self,incidentType):
		items = {
		"incidentType":incidentType
		}
		if items["incidentType"]=="redflag" or items["incidentType"] == "intervention":
			return True
		return "invalid field data"

	def validate_mediaType(self,media):
		items = {
		"media" : media
		}
		if items["media"]=="image" or items["media"] == "video":
			return True
		return "invalid media data"
	def check_comment(self,comment):
		"""Function checks if the string contains any special character """
		items = {
		"comment":comment,	
		}
		if type(comment) == int:
			return True
		regex = re.compile('[@_!#$%£^&*()<>?/|}{~:]')
		"""Make own character set and pass this as argument in compile method """
		if(regex.search(comment)==None):
			""" Pass the string in search method of regex object"""		
			return True
		return "err"

	def check_location(self,location):
		items = {
		"location": location
		}
		if type(location) == int:
			return True
		regex = re.compile('[@_!#$%£^&*()<>?/|}{~:]')
		"""Make own character set and pass this as argument in compile method """
		if(regex.search(location)==None):
			""" Pass the string in search method of regex object"""
			return True
		return "err"

	def check_type(self,location,comment):
		items = {
		"location" : location,
		"comment" : comment
		}
		for items in items:
			if type(location) != str or type(comment) != str:
				return "invalid data"
			return True

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
		return "no match"

	def edit(self, incident_id):
		for incident in incidents:
			if incident["id"] == incident_id:
				resp = self.check_empty_fields()
				if resp == "invalid data":
					return "invalid data"
				resp = self.validate_incidentType_edit()
				if resp == "invalid data":
					return "invalid data"
				resp = self.validate_media_edit()
				if resp == "invalid data":
					return "invalid data"
				resp = self.validate_special_char_comment()
				if resp == "invalid data":
					return "invalid data"
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
		items = request.get_json(force=True)
		incidentType = items["incidentType"]
		location = items["location"]
		comment = items["comment"]
		resp_one = self.validate_fields(incidentType, location,comment)
		if resp_one == "null fields":
			return "invalid data"

	def validate_incidentType_edit(self):
		items = request.get_json(force=True)
		incidentType = items["incidentType"]
		resp = self.validate_incidentType(incidentType)
		if resp == "invalid field data":
			return "invalid data"

	def validate_media_edit(self):
		items = request.get_json(force=True)
		media = items["media"]
		resp = self.validate_mediaType(media)
		if resp == "invalid media data":
			return "invalid data"

	def validate_special_char_comment(self):
		items = request.get_json(force=True)
		comment = items["comment"]
		resp = self.check_comment(comment)
		if resp == "err":
			return "invalid data"

	def validate_special_char_location(self):
		items = request.get_json(force=True)
		location = items["location"]
		resp = self.check_location(location)
		if resp == "err":
			return "invalid data"

	def validate_type(self):
		items = request.get_json(force=True)
		for item in items:
			newval = items["location"]
			newval2 = items["comment"]
		resp = self.check_type(newval,newval2)
		if resp == "invalid data":
			return "invalid data"
