'''Create app'''

from flask_api import FlaskAPI
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


#init
db = SQLAlchemy()

from instance.config import configurations
from app.api.v1.views import IncidentsResource,IncidentResource
from app.api.v2.views import incident,incidents

def create_app(configure):
    '''Create the flask app.'''
    app = FlaskAPI(__name__,instance_relative_config=True)
    app.config.from_object(configurations[configure])
    app.url_map.strict_slashes = False
    api = Api(app)
    api.add_resource(IncidentsResource, '/api/v1/incidents')
    api.add_resource(IncidentResource,'/api/v1/incidents/<int:incident_id>')
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/incidents', methods=['POST', 'GET'])
    def route_incident():
        return incidents()
    @app.route('/incidents/<int:id>', methods=['DELETE', 'PUT','GET'])
    def route_incident_manipulation(id):
        return incident(id)
    
    from auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app


