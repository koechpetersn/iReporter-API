'''Create app'''

from flask_api import FlaskAPI
from flask_restful import Api


from instance.config import configurations
from app.v1.views import IncidentsResource,IncidentResource

def create_app(configure):
    '''Create the flask app.'''
    app = FlaskAPI(__name__,instance_relative_config=True)
    #revisit
    #revist
    #revist
    #revisit
    app.config.from_object(configurations[configure])
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()
    api = Api(app)
    api.add_resource(IncidentsResource, '/api/v1/incidents')
    api.add_resource(IncidentResource,'/api/v1/incidents/<int:incident_id>')
    app.config.from_pyfile('config.py')
    
    from app.v2.views import view_blueprint
    app.register_blueprint(view_blueprint)

    return app


