"""users"""
from . import auth_blueprint

from flask.views import MethodView
from flask_restful import Resource
from flask import make_response, request, jsonify

from app.v2.models.user_models import UserModel



class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/register"""

        # Query to see if the user already exists
        email=request.data['email']
        # user = User.query.filter_by(email=request.data['email']).first()
        user = UserModel.get(email=email)
        print (user)

        if not user:
            # There is no user so we'll try to register them
            try:
                post_data = request.data
                # Register the user
                email = post_data['email']
                name = post_data['name']
                password = post_data['password']
                role = post_data['role']
                new_user = UserModel(name=name,email=email, password=password, role=role)
                new_user.add_user()

                response = {
                    'message': 'You registered successfully. Please log in.',
                    'user':new_user.view()
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
                'user':user[2]
            }

            return make_response(jsonify(response)), 202

class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/login"""
        try:
            # post_data = request.get_json()
            email=request.data['email']
            password=request.data["password"]
            
            # Get the user object using their email (unique to every user)
            user = UserModel.get(email=email)
            print(user)
            
            # Try to authenticate the found user using their password
            if user:
                user = UserModel(email=email,name=user[2],password=user[3],role=user[1])

                
                if not user.password_is_valid(email,password):
                    return "wrong"
                

                # supplied_password=request.data['password']
                # db_user_password = UserModel.get(email=email)[4]

                # import pdb; pdb.set_trace()
                # if db_user_password:
                #     validation = UserModel.password_is_valid(email=email,password=supplied_password)

                # # login_user_data = UserModel(email=email,name=user[2],role=user[1],password=user[4])
                # # import pdb; pdb.set_trace()
                # # boool = login_user_data.password_is_valid(email,supplied_password)
                # # import pdb; pdb.set_trace()
                # print(validation)
                # if validation == False:
                #     return {"message":"wrong password"},401

                id = UserModel.get(email=email)[0]
            
                # Generate the access token. This will be used as the authorization header
                access_token = login_user_data.generate_token(email)
                # import pdb; pdb.set_trace()
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
        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)