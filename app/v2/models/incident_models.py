
from os import getenv
from time import time
from psycopg2.extras import RealDictCursor

from app.v2.db_con import db_connection

conn = db_connection(getenv("DB_NAME"))
conn.set_session(autocommit=True)
curr = conn.cursor(cursor_factory=RealDictCursor)

class IncidentModel():
    """incident model"""
    def __init__(self,comment,location,created_by):
        self.comment=comment
        self.location=location
        self.created_by=created_by
    
    def save(self):
        """save to db"""
        conn.commit()

    def add_incident(self):
        '''Add incident details to table.'''
        curr.execute(
            """
            INSERT INTO incidents (comment, location,created_by)
            VALUES(%s,%s,%s)
            """,
            (self.comment, self.location,self.created_by)
        )
   
        self.save()

    @staticmethod
    def get_all_by(user_id):
        '''Get all incidents by specific user.'''
        query = "SELECT * FROM incidents WHERE created_by={}".format(user_id)
        curr.execute(query)
        incidents = curr.fetchall()
        return incidents

    @staticmethod
    def get_all():
        """Admin get all incidents by all users"""
        query = "SELECT * FROM incidents"
        curr.execute(query)
        incidents = curr.fetchall()
        return incidents

    @classmethod
    def delete_incident(cls, id):
        '''Delete an incident from db.'''
        query = "DELETE FROM incidents WHERE id={}".format(id)
        curr.execute(query)

    def update(self, id, new_data):
        '''Update incident details given new information.'''
        for key, val in new_data.items():
            curr.execute("""
            UPDATE incidents SET {}='{}' WHERE id={}
            """.format(key, val, id))

    @staticmethod
    def get(**kwargs):
        '''Fetch incident by key'''
        for key, val in kwargs.items():
            query = "SELECT * FROM incidents WHERE {}='{}'".format(key, val)
            curr.execute(query)
            incident = curr.fetchone()
            return incident

    @staticmethod
    def view(incident):
        '''View a product information.'''
        id = incident["id"]
        return {
            'id': id,
            'comment': incident["comment"],
            'location': incident["location"],
            'created_by':incident["created_by"]
        }
         