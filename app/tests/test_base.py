'''Base test class.'''
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
        "location" : "fhkdhf",
        "status" : "Draft",
        "media" : "image",
        "comment" : "nothing yet"
        }

    def tearDown(self):
        self.data.clear()
class InvalidTypeInput(TestCase):
    """class to Test invalid input edge case"""

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
    """class to test missing field edge case"""

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
    """class to test special character inclusion edge case"""

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
    """class to test invalid incident type"""

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
