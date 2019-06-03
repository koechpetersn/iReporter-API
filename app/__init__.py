'''Create app and wrap it with Flask'''

from flask_api import FlaskAPI
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

#init
db = SQLAlchemy()

#local imports
from instance.config import configurations
from app.api.v1.views import IncidentsResource,IncidentResource

def create_app(configure):
    '''Create the flask app.'''
    app = FlaskAPI(__name__,instance_relative_config=True)
    app.config.from_object(configurations[configure])
    app.url_map.strict_slashes = False
    app_context = app.app_context()
    app_context.push()
    api = Api(app)
    api.add_resource(
        IncidentsResource,
        '/v1/user/post/incident',
        '/v1/user/get/incidents'
        )
    api.add_resource(
        IncidentResource,
        '/v1/user/get/incident/<int:incident_id>',
        '/v1/user/del/incident/<int:incident_id>',
        '/v1/user/put/incident/<int:incident_id>'
        )
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    from app.api.v2.views import v2_blueprint as version_two
    app.register_blueprint(version_two)

    return app


