'''Tests product resource.'''
import json

from json import loads, dumps

from .test_base import BaseCase, DataCase



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

    """Class to test incidents"""

    def test_can_create_incident(self):

        """Test the POST functionality for an incident creation."""

        response = self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        result = json.loads(response.data)
        expected = "Incident successfully captured"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 201)
    
    def test_can_get_incidents(self):
        """Test the GET functionality of viewing incidents."""
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.get(INCIDENTS_URL)
        result = json.loads(response.data)
        expected = "All incidents available"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
    
    def test_can_get_specific_incident(self):
        """Test the POST functionality for viewing a single incident."""
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.get(INCIDENT_URL)
        result = json.loads(response.data)
        expected = "Incident found!"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
    
class TestSingleIncident(BaseCase):

    def test_can_delete_incidences(self):
        """Test the POST functionality of deleting an incident."""
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.delete(INCIDENT_URL, data=json.dumps(self.data))
        result = json.loads(response.data)
        expected = 'Record deleted successfully'
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)

class TestInvalidData(DataCase):
    """Class to test invalid data"""

    def test_invalid_data(self):
        """Test the robustness of the code if invalid data is supplied."""
        response = self.client.post(INCIDENTS_URL, data=json.dumps(self.invalid_data))
        result = json.loads(response.data)
        expected = "Invalid data, Please enter correct details"
        self.assertEqual(result["msg"], expected)
        self.assertEqual(response.status_code, 400)

     

  

    