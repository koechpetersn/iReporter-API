import jwt
from psycopg2.extras import RealDictCursor
from flask_bcrypt import Bcrypt
import bcrypt
from datetime import datetime, timedelta
from os import getenv
from time import time

from app.v2.db_con import db_connection

conn = db_connection(getenv("APP_SETTINGS"))
conn.set_session(autocommit=True)
curr = conn.cursor(cursor_factory=RealDictCursor)

class UserModel():
    """This class houses User model"""
    def __init__(self,name,email,password,role="normal"):
        self.name=name
        self.email=email
        self.password=Bcrypt().generate_password_hash(password).decode()
        self.role=role

    def save(self):
        '''save item to db'''
        conn.commit()

    def add_user(self):
        '''Add user details to table.'''
        curr.execute(
            """
            INSERT INTO users (name, email, password, role)
            VALUES(%s,%s,%s,%s)
            """,
            (self.name, self.email, self.password, self.role)
        )
        self.save()

    @staticmethod
    def get(**kwargs):
        """get user by key"""
        for key, val in kwargs.items():
            query = "SELECT * FROM users WHERE {}='{}'".format(key,val)
            curr.execute(query)
            user=curr.fetchone()
            return user
    
    @staticmethod
    def get_all():
        """get all users"""
        query = "SELECT * FROM users"
        curr.execute(query)
        users = curr.fetchall()
        return users

    @classmethod
    def delete_user(cls, id):
        '''Delete a user from db.'''
        query = "DELETE FROM users WHERE id={}".format(id)
        curr.execute(query)
        

    @staticmethod
    def password_is_valid(email,password):
        """compare supplied password against stored hash"""

        user = UserModel.get(email=email)
        db_pass = user['password']

        db_byte_pass = bytes(db_pass, 'utf-8')
        supplied_pass = bytes(password, 'utf-8')

        if_password_match = bcrypt.checkpw(supplied_pass,db_byte_pass)
        return if_password_match

    def generate_token(self,email):
        """ Generates the access token"""

        id = UserModel.get(email=email)['id']
        key = getenv('SECRET')

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=36000),
                'iat': datetime.utcnow(),
                'sub': id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                getenv('SECRET'),
                algorithm='HS256'
            )
            
            return jwt_string.decode()

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    def generate_admin_token(self,email):
        """ Generates the admin access token with admin previledges"""

        role = UserModel.get(email=email)['role']
        key = getenv('SECRET')

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=6),
                'iat': datetime.utcnow(),
                'sub': role
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                getenv('SECRET'),
                algorithm='HS256'
            )
            
            return jwt_string.decode()

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        # return jwt.decode(token,key=str(getenv('SECRET')))
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, getenv('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    @staticmethod
    def view(user):
        """view user info"""
        id = user['id']
        return {
            'id':id,
            'name':user["name"],
            'email':user["email"],
            'role':user["role"]
        }

