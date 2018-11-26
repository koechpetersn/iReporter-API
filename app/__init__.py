'''Create app'''

from flask import Flask
from flask_restful import Api

from config import configurations
from app.v1.views import RedflagResource


def create_app():
    '''Create the flask app.'''
    app = Flask(_name_)
    app.config.from_object(configurations["development"])
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()
    api = Api(app)
    api.add_resource(
        ReflagResource, '/api/v1/redflags', '/api/v1/redflags/<int:redflag_id>')
    return app