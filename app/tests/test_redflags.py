'''Tests product resource.'''
import json

from json import loads, dumps

from .test_base import BaseCase



INCIDENTS_URL = '/api/v1/incidents/'

INCIDENT_URL = '/api/v1/incidents/1'





class TestMultipleIncidents(BaseCase):

    """Class to test incidents"""

    def test_can_create_incident(self):

        """Test the POST functionality for a product."""

        response = self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        result = json.loads(response.data)
        expected = "Incident successfully captured"
        #self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 201)
    
    def test_can_get_incidents(self):
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.get(INCIDENTS_URL)
        result = json.loads(response.data)
        expected = "All incidents"
        #self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
    
    def test_can_get_specific_incident(self):
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.get(INCIDENT_URL)
        result = json.loads(response.data)
        expected = "Incident found!"
        #self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
    
class TestSingleIncident(BaseCase):

    def test_can_delete_incidences(self):
        self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
        response = self.client.delete(INCIDENT_URL, data=json.dumps(self.data))
        #result = json.loads(response.data)
        expected = 'Record deleted successfully'
        #self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
     
# class TestEditIncident(BaseCase):  
#     def test_can_edit_incidences(self):
#         self.client.post(INCIDENTS_URL, data=json.dumps(self.data))
#         response = self.client.patch(INCIDENT_URL, data=json.dumps(self.data))
#         result = json.loads(response.data)
#         expected = "Record updated successfully"
#         #self.assertEqual(result["message"], expected)
#         self.assertEqual(response.status_code, 200)
    
  

    