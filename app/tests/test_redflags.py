'''Tests product resource.'''
import json

from .test_base import BaseCase, MissingField, InvalidTypeInput, SpecialChar, IncidentType



INCIDENTS_URL = '/api/v1/incidents/'

INCIDENT_URL = '/api/v1/incidents/1'



class TestEditIncident(BaseCase):
    """class to test EDIT functionality"""
    def test_can_edit_incidences(self):
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.patch(INCIDENT_URL, data=json.dumps(self.data))
        result = json.loads(response.data)
        expected = "Record updated successfully"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
    

class TestMultipleIncidents(BaseCase):
    """Class to test POST and GET functionality"""

    def test_can_create_incident(self):
        """Test the POST functionality."""

        response = self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        result = json.loads(response.data)
        expected = "Incident successfully captured"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 201)
    
    def test_can_get_incidents(self):
        """Test the GET functionality."""
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.get(INCIDENTS_URL)
        result = json.loads(response.data)
        expected = "All incidents available"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
    
    def test_can_get_specific_incident(self):
        """Test the GET functionality for viewing a single incident."""
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.get(INCIDENT_URL)
        result = json.loads(response.data)
        expected = "Incident found!"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
    
class TestSingleIncident(BaseCase):
    """Class to test a specific incident by id"""

    def test_can_delete_incidences(self):
        """Test the DELETE functionality of deleting an incident."""
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.delete(INCIDENT_URL, data=json.dumps(self.data))
        result = json.loads(response.data)
        expected = 'Record deleted successfully'
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)

class TestInvalidData(InvalidTypeInput):
    """Class to test invalid data type"""

    def test_invalid_data_input(self):
        """Test the robustness of the code if invalid data is supplied."""
        response = self.client.post(INCIDENTS_URL, data=json.dumps(self.invalid_type_data))
        result = json.loads(response.data)
        expected = "Only image or video is accepted to media field"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 201)

class TestMissingField(MissingField):
    """Class to test missing field data"""

    def test_missing_fields(self):
        """Test the robustness of the code if some fields are left out."""
        response = self.client.post(INCIDENTS_URL, data=json.dumps(self.missing_field_data))
        result = json.loads(response.data)
        expected = "Missing fields, Please supply data for all fields"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 201)

class TestSpeacialChar(SpecialChar):
    """Class to test special character inclusion in data"""

    def test_special_char_comment(self):
        response = self.client.post(INCIDENTS_URL, data=json.dumps(self.specialchar_data))
        result = json.loads(response.data)
        expected = "Special characters not allowed!"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 201)

    def test_special_char_location(self):
        response = self.client.post(INCIDENTS_URL, data=json.dumps(self.specialchar_data))
        result = json.loads(response.data)
        expected = "Special characters not allowed!"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 201)

class TestIncidentType(IncidentType):
    """Class to test valid incindent type"""
    def test_special_char(self):
        response = self.client.post(INCIDENTS_URL, data=json.dumps(self.incidents_data))
        result = json.loads(response.data)
        expected = "Only redflag or intervention is accepted to incidentType field"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 201)
