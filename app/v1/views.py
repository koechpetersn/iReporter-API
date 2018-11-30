from flask_restful import Resource, reqparse

from app.v1.models import Incident, db

class IncidentResource(Resource):
	'''class for handling incidents'''
	parser = reqparse.RequestParser()
	parser.add_argument('title',required=True,type=str,help='title(str) is required')
	parser.add_argument('nature',required=True,type=str,help='nature(str) is required')
	parser.add_argument('comment',required=True,type=str,help='comment(str) is required')

	@classmethod
	def post(cls):
		arguments = IncidentResource.parser.parse_args()
		title = arguments.get('title')
		nature = arguments.get('nature')
		comment = arguments.get('comment')

		# for redflag in getattr(db,'redflags'):
		# 	if title == redflag['title']:
		# 		return {
		# 		'message' : 'Redflag with that title already exists'
		# 		}, 409
		
		incident = Incident(title = title, nature = nature, comment = comment)
		incident = incident.save()
		return {
				'message' : 'Redflag successfully added','incident' : incident
				}, 201

	# def get(cls):
	# 	resp = self