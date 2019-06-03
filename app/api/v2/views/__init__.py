# auth/__init__.py

from flask import Blueprint

# This instance of a Blueprint that represents the authentication blueprint
v2_blueprint = Blueprint('v2', __name__)

from . import user_auth
from . import manage_users
from . import manage_incidents
