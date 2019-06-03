"""User Models"""

from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import jwt
from app import db
from os import getenv


class UserModel(db.Model):
    """This class houses user model"""

    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255))
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_registered = db.Column(db.DateTime, default=db.func.current_timestamp())
    incidents = db.relationship('IncidentModel', order_by='IncidentModel.id', cascade="all, delete-orphan")

    def __init__(self,email,password,role="normal"):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.role=role
    
    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def view(self):
        '''def'''
        return {
            'email':self.email,
            'role':self.role,
            'id':self.id
        }


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_user(user_id):
        return UserModel.query.filter_by(id=user_id).first()

    @staticmethod
    def get_all():
        return UserModel.query.all()

    def delete(self):
        """Deletes a given user."""
        db.session.delete(self)
        db.session.commit()
    
    def generate_token(self,user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=36000000),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                getenv('SECRET'),
                algorithm='HS256'
            )
            
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    def generate_admin_token(self,role):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=36000000),
                'iat': datetime.utcnow(),
                'sub': role
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                getenv('SECRET'),
                algorithm='HS256'
            )
            
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        # return jwt.decode(token,key=str(getenv('SECRET')))
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, getenv('SECRET'),algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

class IncidentModel(db.Model):
    """This class represents the incidents table"""
    
    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)
    incidentType = db.Column(db.String(255),default="redflag")
    description = db.Column(db.String(255))
    location = db.Column(db.String(255))
    status = db.Column(db.String(255), default="Draft")
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    
    def __init__(self,description,location,created_by):
        """initialize with data."""
        self.description = description
        self.location = location
        self.created_by = created_by
    
    def save(self):
        """save item to db"""
        db.session.add(self)
        db.session.commit()

    def view(self):
        '''def'''
        return {
            'ID':self.id,
            'incident type':self.incidentType,
            'status':self.status,
            'description':self.description,
            'location':self.location,
            'Date created':self.date_created,
            'Date modified':self.date_modified,
            'Created by':self.created_by
        }

    @staticmethod
    def get_all(user_id):
        return IncidentModel.query.filter_by(created_by=user_id)

    @staticmethod
    def admin_get_all():
        return IncidentModel.query.all()

    @staticmethod
    def admin_get_specific(incident_id):
        return IncidentModel.query.filter_by(id=incident_id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # def __repr__(self):
    #     return "<Incident: {}>".format(self.incidentType)

