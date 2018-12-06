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
class InvalidTypeInput(TestCase):

    def setUp(self):

        self.app = create_app()

        self.client = self.app.test_client()

        self.invalid_type_data = {
        "id" : 1,
        "createdBy" : 1,
        "incidentType" : "redflag",
        "location" : "Mombasa",
        "status" : "Draft",
        "media" : 78,
        "comment" : "data"
        }
class MissingField(TestCase):

    def setUp(self):

        self.app = create_app()

        self.client = self.app.test_client()

        self.missing_field_data = {
        "id" : 1,
        "createdBy" : 1,
        "incidentType" : "",
        "location" : "Nakuru",
        "status" : "Draft",
        "media" : "image",
        "comment" : "data"
        }
class SpecialChar(TestCase):

    def setUp(self):
        self.app = create_app()

        self.client = self.app.test_client()

        self.specialchar_data = {
        "id" : 1,
        "createdBy" : 1,
        "incidentType" : "redflag",
        "location" : "Nakuru%)",
        "status" : "Draft",
        "media" : "image",
        "comment" : "sj%"
        }
class IncidentType(TestCase):

    def setUp(self):
        self.app = create_app()

        self.client = self.app.test_client()

        self.incidents_data = {
        "id" : 1,
        "createdBy" : 1,
        "incidentType" : "redflaG1",
        "location" : "Nakuru",
        "status" : "Draft",
        "media" : "image",
        "comment" : "sj%"
        }


