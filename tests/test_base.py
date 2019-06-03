from unittest import TestCase
from app import create_app
from app.api.v1.models import db

class BaseCase(TestCase):
    '''Base class to be inherited by all other testcases.'''

    def setUp(self):

        '''Set up test application.'''

        self.app = create_app(configure="testing")

        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.data = {
        "location" : "fhkdhf",
        "description" :"hdshgh"
        }

        self.data2 = {
        "location" : "Nakuru",
        "description" : "sj%"
        }

        self.invalid_type = {
        "location" : "Mombasa",
        "description" : 89
        }

        self.empty_field_data = {
        "description" : "Nakuru",
        "location":""

        }

        self.whitespace_data = {
        "description" : "Nakuru",
        "location":" "

        }

        self.specialchar_data = {
        "location" : "n&*&ds",
        "description" : "dfg"
        }


    def tearDown(self):
        '''Delete database and recreate it with no data.'''
        db.drop()
        self.app_context.pop()
        










