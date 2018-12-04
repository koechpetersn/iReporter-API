'''Base test class.'''
import json
import datetime
from unittest import TestCase
from app import create_app


class BaseCase(TestCase):
    '''Base class to be inherited by all other testcases.'''

    def setUp(self):

        '''Set up test application.'''

        self.app = create_app()

        self.client = self.app.test_client()

        self.data = {
        "id" : 1,
        "createdBy" : 1,
        "incidentType" : "redflag",
        "location" : "2345",
        "status" : "Draft",
        "media" : "image",
        "comment" : "nothing yet"
        }
class DataCase(TestCase):

    def setUp(self):

        self.app = create_app()

        self.client = self.app.test_client()

        self.invalid_data = {
        "id" : 1,
        "createdBy" : 1,
        "incidentType" : "redflag",
        "location" : 234,
        "status" : "Draft",
        "media" : 45,
        "comment" : True
        }



