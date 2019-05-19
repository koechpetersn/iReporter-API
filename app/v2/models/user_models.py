import jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from os import getenv
from time import time

from app.v2.db_con import db_connection

conn = db_connection(getenv("DB_NAME"))
conn.set_session(autocommit=True)
curr = conn.cursor()

class UserModel():
    """docs"""
    def __init__(self,name,email,password,role):
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

    def delete_user(self, id):
        '''Delete a user from db.'''
        query = "DELETE FROM users WHERE id={}".format(id)
        cur.execute(query)
        self.save()

    @staticmethod
    def password_is_valid(email, password):
        """compare hashes"""
        # return Bcrypt().check_password_hash(self.password, password)

        user_pass = UserModel.get(email=email)
        
        # print(Bcrypt().generate_password_hash(password))
        return True if Bcrypt().generate_password_hash(password) == user_pass[3] else False
        
    def delete_user(self,id):
        query = "DELETE FROM users WHERE id={}".format(id)
        curr.execute(query)
        self.save()

    def generate_token(self,email):
        """ Generates the access token"""

        id = UserModel.get(email=email)[0]
        key = getenv('SECRET')

        # payload = {
        #     'user_id':id
        #     }
        # return jwt.encode(payload=payload,key=str(key),algorithm='HS256').decode()

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=120),
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
    
    def view(self):
        """view user info"""
        id = UserModel.get(email=self.email)[0]
        return {
            'id':id,
            'name':self.name,
            'email':self.email,
            'role':self.role
        }

