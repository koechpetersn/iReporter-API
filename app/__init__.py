'''Create app'''

from flask import Flask
from flask_restful import Api

from config import configurations
<<<<<<< HEAD
from app.v1.views import IncidentResource
=======
from app.api.v1.views import IncidentsResource,IncidentResource
>>>>>>> caaa84061e6d956fa538d2986a8d89bfd0fdd02d


def create_app():
    '''Create the flask app.'''
    app = Flask(__name__)
    app.config.from_object(configurations["development"])
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()
    api = Api(app)
<<<<<<< HEAD
    api.add_resource(
        IncidentResource, '/api/v1/incidents', '/api/v1/incidents/<int:incident_id>')
    return app
=======
    api.add_resource(IncidentsResource, '/api/v1/incidents')
    api.add_resource(IncidentResource,'/api/v1/incidents/<int:incident_id>')
    return app
>>>>>>> caaa84061e6d956fa538d2986a8d89bfd0fdd02d
