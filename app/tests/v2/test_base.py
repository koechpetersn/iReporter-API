'''Base test class.'''
from unittest import TestCase
# from flask import g
import psycopg2

from app.v2.models.user_models import UserModel
# import os
# import json

from app.v2.db_con import create, db_connection,incidents_table,user_table
from app import create_app

class BaseTest(TestCase):
    """Base class for testcases"""
    def setUp(self):
        # conn = db_connection(os.getenv("TESTING_DB"))
        # cur = conn.cursor()
        # user_table(cur)
        # incidents_table(cur)
        # cur.close()
        # conn.commit()
        # conn.close()
        self.app = create_app(configure="testing")
        import pdb; pdb.set_trace()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        # initialize the test client
        
        
        
        self.user_data = {
            'email': 'example@example.com',
            'name':'tester',
            'password': 'pass1234'
        }

        # with self.app.app_context():
        #     # create all tables
        #     conn = db_connection('test_db')
        #     cur = conn.cursor()
        #     cur.execute("""DROP TABLE IF EXISTS users CASCADE;""")
        #     cur.execute(  """DROP TABLE IF EXISTS  incidents CASCADE;""")
            
        #     conn.commit()
        #     user_table(cur)
        #     incidents_table(cur)
        #     cur.close()
        #     conn.commit()
        #     conn.close()


    # def tearDown(self):
    #     """Delete database and recreate it with no data."""
