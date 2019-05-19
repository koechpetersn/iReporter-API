
from os import getenv
from time import time

from app.v2.db_con import db_connection

conn = db_connection(getenv("DB_NAME"))
conn.set_session(autocommit=True)
curr = conn.cursor()

class Incident():
    """incident model"""
    def __init__(self,comment,location):
        self.comment=comment
        self.location=location
    
    def save(self):
        """save to db"""
        conn.commit()

    def add_incident(self):
        '''Add incident details to table.'''
        curr.execute(
            """
            INSERT INTO incidents (comment, location)
            VALUES(%s,%s)
            """,
            (self.comment, self.location)
        )
   
        self.save()

    @staticmethod
    def get_all():
        '''Get all incidents.'''
        query = "SELECT * FROM incidents"
        cur.execute(query)
        incidents = cur.fetchall()
        return incidents

    @classmethod
    def delete(cls, id):
        '''Delete an incident from db.'''
        query = "DELETE FROM incidents WHERE id={}".format(id)
        cur.execute(query)

    def update(self, id, new_data):
        '''Update incident details given new information.'''
        for key, val in new_data.items():
            cur.execute("""
            UPDATE incidents SET {}='{}' WHERE id={}
            """.format(key, val, id))

    @staticmethod
    def get(**kwargs):
        '''Fetch incident by key'''
        for key, val in kwargs.items():
            query = "SELECT * FROM incidents WHERE {}='{}'".format(key, val)
            cur.execute(query)
            incident = cur.fetchone()
            return incident

    @staticmethod
    def view(incident):
        '''View a product information.'''
        id = incident[0]
        return {
            'id': id,
            'comment': incident[1],
            'location': incident[2],
            'created_by':incident[3]
        }
         