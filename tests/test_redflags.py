'''Tests product resource.'''
import json

from tests.test_base import BaseCase

POST_URL = '/v1/user/post/incident'
GET_URL = 'v1/user/get/incident/1'

class TestEditIncident(BaseCase):
    """class to test EDIT functionality"""

    def test_can_create_incident(self):
        """Test the POST functionality."""
        response = self.client.post(POST_URL, data=json.dumps(self.data))
        result = json.loads(response.data)
        expected = "Incident reported successfully"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 201)
    
    def test_can_get_incidents(self):
        """Test the GET functionality."""
        self.client.post(POST_URL, data=json.dumps(self.data))
        self.client.post(POST_URL, data=json.dumps(self.data2))
        response = self.client.get('/v1/user/get/incidents')
        result = json.loads(response.data)
        expected = "Incidents found"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
    
    def test_can_get_specific_incident(self):
        """Test the GET functionality for viewing a single incident."""
        self.client.post(POST_URL, data=json.dumps(self.data))
        response = self.client.get(GET_URL)
        result = json.loads(response.data)
        expected = "Incident found"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)

    def test_can_edit_incidences(self):
        resp = self.client.post(POST_URL, data=json.dumps(self.data))
        response = self.client.patch('/v1/user/put/incident/1', data=json.dumps(self.data2))
        result = json.loads(response.data)
        expected = "Record updated successfully"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.patch('/v1/user/put/incident/1', data=json.dumps(self.invalid_type))
        result = json.loads(response2.data)
        expected2 = "Description must be a string and not integer"
        self.assertEqual(result["message"], expected2)
        self.assertEqual(response2.status_code, 401)
    
    def test_can_delete_incidences(self):
        """Test the DELETE functionality of deleting an incident."""
        self.client.post(POST_URL, data=json.dumps(self.data))
        response = self.client.delete('/v1/user/del/incident/1')
        result = json.loads(response.data)
        expected = 'Record deleted successfully'
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(GET_URL)
        result = json.loads(response.data)
        expected = "Incident not found"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 404)

    def test_can_catch_invalid_data_input_error(self):
        """Test the robustness  if invalid data type is supplied."""
        response = self.client.post(POST_URL, data=json.dumps(self.invalid_type))
        result = json.loads(response.data)
        expected = "Description must be a string and not integer"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 401)

    def test_can_reject_special_char_input(self):
        response = self.client.post(POST_URL, data=json.dumps(self.specialchar_data))
        result = json.loads(response.data)
        expected = "Special characters not allowed!"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 401)

    def test_can_reject_empty_strings(self):
        response = self.client.post(POST_URL, data=json.dumps(self.empty_field_data))
        result = json.loads(response.data)
        expected = "Location cannot be blank"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 401)

    def test_can_reject_whitespaces(self):
        response = self.client.post(POST_URL, data=json.dumps(self.whitespace_data))
        result = json.loads(response.data)
        expected = "Location cannot be left blank"
        self.assertEqual(result["message"], expected)
        self.assertEqual(response.status_code, 401)

