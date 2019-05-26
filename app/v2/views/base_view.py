from flask import request

from app.v2.models.incident_models import IncidentModel
from app.v2.models.user_models import UserModel

class Base():
    """Base class to extract auth headers"""
    @classmethod
    def helper(cls):
        """decode token"""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
            payload = UserModel.decode_token(access_token)
            return payload

        else:
            response = "You are not authorized to perform this operation"
            return response