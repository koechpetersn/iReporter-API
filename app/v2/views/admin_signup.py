"""This module houses Admin Registration and Login models"""
from . import view_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify

from app.v2.models.user_models import UserModel

class AdminSignup(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/register"""

        # Pull registration data
        email=request.data['email']
        # Query to see if the user already exists
        user = UserModel.get(email=email)

        if not user:
            # There is no user so we'll try to register them
            try:
                post_data = request.data
                # Register the user
                email = post_data['email']
                name = post_data['name']
                password = post_data['password']
                
                new_user = UserModel(name=name,email=email, password=password,role="admin")
                new_user.add_user()
                response = {'message': 'You registered successfully. Please log in to proceed.'}
                
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.',
                'user':user["email"]
            }

            return make_response(jsonify(response)), 202

admin_signup_view = AdminSignup.as_view('admin_signup_view')

view_blueprint.add_url_rule(
    '/v2/admin/signup',
    view_func=admin_signup_view,
    methods=['POST'])