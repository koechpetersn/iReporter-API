"""This module houses Registration and Login models"""
from . import view_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify

from app.v2.models.user_models import UserModel


class UserSignin(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/login"""
        # try:
        
        email=request.data['email']
        password=request.data["password"]
        
        # Get the user object using their email (unique to every user)
        user = UserModel.get(email=email)
        # Try to authenticate the found user using their password
        
        if user:
            user = UserModel(email=email,name=user['name'],password=user['password'],role=user['role'])
            print(user.password)
            valid_resp = user.password_is_valid(email,password)
            print(valid_resp)

            if not valid_resp:
                response = {
                    "message":"The password is incorrect, Please provide a correct password"
                } 
                return make_response (jsonify(response)), 401
    
            # Generate the access token. This will be used as the authorization header
            access_token = user.generate_token(email)

            if access_token:
                response = {
                    'message': 'You logged in successfully.',
                    'access_token': access_token
                }
                return make_response(jsonify(response)), 200
        else:
            # User does not exist. Therefore, we return an error message
            response = {
                'message': 'Email not registred'
            }
            return make_response(jsonify(response)), 401
            
        # except Exception as e:
        #     # Create a response containing an string error message
        #     response = {
        #         'message': str(e)
        #     }
        #     # Return a server error using the HTTP Error Code 500 (Internal Server Error)
        #     return make_response(jsonify(response)), 500


user_signin_view = UserSignin.as_view('user_signin_view')
# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
view_blueprint.add_url_rule(
    '/v2/user/signin',
    view_func=user_signin_view,
    methods=['POST']
)