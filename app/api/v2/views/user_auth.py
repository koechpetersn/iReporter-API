"""User auth"""
from . import v2_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.api.v2.models.models import UserModel

class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /v2/user/signup"""

        # Query to see if the user already exists
        user = UserModel.query.filter_by(email=request.data['email']).first()
        
        if not user:
            # There is no user so we'll try to register them
            try:
                post_data = request.data
                # Register the user
                email = post_data['email']
                password = post_data['password']
                user = UserModel(email=email, password=password, role = "normal")
                user.save()
                response = {
                    'message': 'You registered successfully. Please log in.',
                    'user':user.view()
                }
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
                'user':user.view()
            }

            return make_response(jsonify(response)), 202
            
class AdminRegistrationView(MethodView):
    """This class registers a new admin user."""

    def post(self):
        """ Handle POST request for this view. Url ---> /v2/admin/signup
            URLS for admin registration are protected during front-end implementation
        """

        # Query to see if the user already exists
        user = UserModel.query.filter_by(email=request.data['email']).first()
        if not user:
            # There is no user so we'll try to register them
            try:
                post_data = request.data
                # Register the user
                email = post_data['email']
                password = post_data['password']
                user = UserModel(email=email, password=password,role="admin")
                # print(user)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.',
                    'user':user.view()
                }
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
                'user':user.view()
            }

            return make_response(jsonify(response)), 401

class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /v2/user/signin"""
        try:
            # post_data = request.get_json()

            # Get the user object using their email (unique to every user)
            user = UserModel.query.filter_by(email=request.data['email']).first()
            # Try to authenticate the found user using their password
            if user and user.password_is_valid(request.data['password']):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                # import pdb; pdb.set_trace()
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'user access token': access_token.decode('utf-8'),
                        'user id':user.id
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

class AdminLogin(MethodView):
    """Handles admin login and access token generation."""
    def post(self):
        """Handle POST request for thus view. Url ---> /v2/admin/signin"""
        user = UserModel.query.filter_by(email=request.data['email']).first()
        if user and user.password_is_valid(request.data['password']):
            check_role = user.role if user else None
            if check_role == "admin":
                access_token = user.generate_admin_token(check_role)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'admin access token': access_token.decode('utf-8')
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    "message":"Not admin user! Please login as a normal user"
                }
                return make_response(jsonify(response)), 401

        else:
            # User does not exist. Therefore, we return an error message
            response = {
                'message': 'Invalid email or password, Please try again'
            }
            return make_response(jsonify(response)), 401

# Define the rule for the registration url
# Then add the rule to the blueprint
registration_view = RegistrationView.as_view('register_view')
admin_registration_view = AdminRegistrationView.as_view('admin_register_view')
login_view = LoginView.as_view('login_view')
admin_signin_view = AdminLogin.as_view('admin_signin_view')

v2_blueprint.add_url_rule(
    '/v2/admin/signin',
    view_func=admin_signin_view,
    methods=['POST']
)

v2_blueprint.add_url_rule(
    '/v2/user/signup',
    view_func=registration_view,
    methods=['POST'])

v2_blueprint.add_url_rule(
    '/v2/admin/signup',
    view_func=admin_registration_view,
    methods=['POST'])

v2_blueprint.add_url_rule(
    '/v2/user/signin',
    view_func=login_view,
    methods=['POST']
)