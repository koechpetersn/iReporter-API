'''Create app'''

from flask import Flask
from flask_restful import Api

from config import configurations
from app.v1.views import IncidentResource


def create_app():
    '''Create the flask app.'''
    app = Flask(__name__)
    app.config.from_object(configurations["development"])
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()
    api = Api(app)
    api.add_resource(
        IncidentResource, '/api/v1/incidents', '/api/v1/incidents/<int:incident_id>')
    return app