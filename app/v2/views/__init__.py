"""views/__init__.py"""

from flask import Blueprint

# This instance of a Blueprint that represents the authentication blueprint
view_blueprint = Blueprint('view', __name__)

from . import user_signup
from . import user_signin
from . import user_reports
from . import admin_signup
from . import admin_signin
from . import manage_users
from . import manage_incidents
