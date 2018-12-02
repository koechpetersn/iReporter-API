'''Base test class.'''
import json
from unittest import TestCase
from app import create_app



class BaseCase(TestCase):

    '''Base class to be inherited by all other testcases.'''



    def setUp(self):

        '''Set up test application.'''

        self.app = create_app()

        self.client = self.app.test_client()

        # self.app_context = self.app.app_context()

        # self.app_context.push()

        self.data = {
        "id" : 1,
        #"createdBy" : 1,
        "incidentType": "redflag",
        "location" : "2345",
        "status" : "Draft",
        "comment" : "nothing yet",
        }

        



    # def tearDown(self):


    #     '''Delete database and recreate it with no data.'''

    #     self.data.clear()

    #     self.app_context.pop()