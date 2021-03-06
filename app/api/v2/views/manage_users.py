from . import v2_blueprint

from flask.views import MethodView
from flask import request, jsonify, abort, make_response
from .base import Base

from app.api.v2.models.models import UserModel

class FetchUsers(MethodView,Base):
    """This class allows an admin to fetch all users in user database"""

    def get(self):
        
        payload = FetchUsers.helper()
        if payload == "admin":
            users = UserModel.get_all()
            if users:
                results=[UserModel.view(user) for user in users]
                return {"all registered users":results},200
            return{"message":"There are no registered users"},404
        return {"message":"You are not allowed to access user database"},401

class FetchUser(MethodView,Base):
    """This class allows admin to fetch a single user by user id"""
    def get(self,user_id):
        """fetch a user"""
        payload = FetchUser.helper()
        if payload == "admin":
            users = UserModel.get_all()
            if users:
                user = [UserModel.view(user) for user in users if user.id==user_id]
                if not user == None:
                    return {"message":user},200
                return {"message":"There is no user with that id"},404
            return {"message":"There are no registered users"},404
        return{"message":"you are not allowed to access user database"},401
                     
class FetchUserBy(MethodView,Base):
    """This class handles how admin user fetches users by user role"""
    def get (self,role):
        """get all users of specific role"""
        payload = FetchUserBy.helper()
        if payload == "admin":
            users = UserModel.get_all()
            if users:
                users = [UserModel.view(user) for user in users if user.role==role]
                return users,200
            return{"message":"There are no registered users"},404
        return {"message":"You are not allowed to access user database"},401

class UserDel(MethodView,Base):
    """Admin can delete a user from database"""
    def delete(self,user_id):
        """delete user"""
        payload = UserDel.helper()
        if payload == "admin":
            user = UserModel.get_user(user_id)
            if user:
                user.delete()
                return {"message":"User successfully deregistered"},200
            return {"message":"User not registered"},404
        return {"message":"You have insufficient rights"},401



# Define the rule for the registration url
# Then add the rule to the blueprint
fetch_users = FetchUsers.as_view('fetch_users')
fetch_user = FetchUser.as_view('fetch_user')
fetch_user_by = FetchUserBy.as_view('fetch_user_by')
del_user = UserDel.as_view("del_user")


v2_blueprint.add_url_rule(
    '/v2/admin/get/users',
    view_func=fetch_users,
    methods=['GET'])

v2_blueprint.add_url_rule(
    '/v2/admin/get/user/<int:user_id>',
    view_func=fetch_user,
    methods=['GET'])

v2_blueprint.add_url_rule(
    '/v2/admin/get/users/<role>',
    view_func=fetch_user_by,
    methods=['GET'])

v2_blueprint.add_url_rule(
    '/v2/admin/del/user/<int:user_id>',
    view_func=del_user,
    methods=['DELETE'])