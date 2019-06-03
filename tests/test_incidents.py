# tests/test_app.py
import unittest
import json
from app import create_app, db

POST_URL = '/v2/user/post/incident'
GET_URL = '/v2/user/get/incident/1'

class IncidentTestCase(unittest.TestCase):
    """This class represents the incident test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(configure="testing")
        self.client = self.app.test_client

        self.incident_one = {
            'description': 'Broken bridge',
            'location': 'Ngong'
        }

        self.incident_two = {
            'description': 'Area chief requests bribe for services',
            'location': 'Kilimani'
        }

        self.empty_field = {
        "description" : "Broken bridge",
        "location":""
        }

        self.whitespace_data = {
        "description" : "Broken bridge",
        "location":" "

        }
        self.invalid_type = {
        "location" :"Broken bridge",
        "description" : True
        }

        self.special_char = {
        "location" : "n&*&ds",
        "description" : "dfg"
        }

        self.user_data_1 = {
            'email': 'test@example.com',
            'password': 'test_password'
        }

        self.user_data_2 = {
            'email':'example@admin',
            'password' : 'passpass'
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_admin_user(
        self,
        email="user@admin.com",
        password="test1234"):
        """This helper method helps register an admin test user."""

        admin_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/v2/admin/signup', data=admin_data)

    def register_user(
        self,
        email="user@test.com",
        password="test1234"):
        """This helper method helps register a test user."""

        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/v2/user/signup', data=user_data)

    def register_user2(
        self,
        email="user2@test.com",
        password="test1234"):
        """This helper method helps register a test user."""

        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/v2/user/signup', data=user_data)

    def login_admin_user(
        self,
        email="user@admin.com",
        password="test1234"):
        """This helper method helps log in an admin test user."""

        admin_user_data = {
            'email': email,
            'password': password
        }
        return self.client().post(
            '/v2/admin/signin',
            data=admin_user_data)
    
    def login_user(
        self,
        email="user@test.com",
        password="test1234"):
        """This helper method helps log in a test user."""

        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/v2/user/signin', data=user_data)

    def login_user2(
        self,
        email="user2@test.com",
        password="test1234"):
        """This helper method helps log in a test user."""

        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/v2/user/signin', data=user_data)

    def test_incident_creation(self):
        """Test API can create an incident (POST request)"""
        # register a test user, then log them in
        self.register_user()
        # obtain the access token
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']
        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
        )
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Ngong', str(resp.data))

    def test_can_reject_empty_strings(self):
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']
        post_resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.empty_field)
        result = json.loads(post_resp.data.decode('utf-8'))
        # import pdb; pdb.set_trace()
        self.assertEqual(post_resp.status_code, 401)
        expected = "Location cannot be blank"
        self.assertEqual(result["message"], expected)

    def test_can_reject_whitespaces(self):
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']
        post_resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.whitespace_data)
        result = json.loads(post_resp.data.decode('utf-8'))
        # import pdb; pdb.set_trace()
        self.assertEqual(post_resp.status_code, 401)
        expected = "Location cannot be left blank"
        self.assertEqual(result["message"], expected)

    def test_can_reject_special_char_input(self):
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']
        post_resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.special_char)
        result = json.loads(post_resp.data.decode('utf-8'))
        # import pdb; pdb.set_trace()
        self.assertEqual(post_resp.status_code, 401)
        expected = "Special characters not allowed!"
        self.assertEqual(result["message"], expected)

    def test_user_can_get_all_own_incidents(self):
        """Test API can get all incidents (GET request)."""
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']
        # create a incidents by making a POST request
        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)

        resp_2 = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_two
            )
        self.assertEqual(resp_2.status_code, 201)
        # get all the incidents that belong to the test user
        get_resp = self.client().get(
            '/v2/user/get/incidents',
            headers=dict(Authorization="Bearer " + token)
            )
        self.assertEqual(get_resp.status_code, 200)
        self.assertIn('Kilimani', str(get_resp.data))
        self.assertIn('Ngong', str(get_resp.data))

    def test_user_can_get_own_incident_by_id(self):
        """Test API can get a single incidents by using it's id."""
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']

        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)
        # get the response data in json format
        result = self.client().get(
            GET_URL,
            headers=dict(Authorization="Bearer " + token)
            )
        # assert that the incidents is actually returned given its ID
        self.assertEqual(result.status_code, 200)
        self.assertIn('Ngong', str(result.data))

    def test_admin_can_get_specific_incident_by_id(self):
        """Test API can get a single incidents by using it's id."""
        self.register_admin_user()
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']

        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)
        # get the response data in json format
        admin_login = self.login_admin_user()
        admin_token = json.loads(admin_login.data.decode())['admin access token']

        result = self.client().get(
            '/v2/admin/get/incident/1',
            headers=dict(Authorization="Bearer " + admin_token)
            )
        # assert that the incidents is actually returned given its ID
        self.assertEqual(result.status_code, 200)
        self.assertIn('Ngong', str(result.data))

    def test_incidents_can_be_edited(self):
        """Test API can edit an existing incidents. (PUT request)"""
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']

        # first, we create a incidents by making a POST request

        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)
        # get the json with the incident
        results = json.loads(resp.data.decode())

        # then, we edit the created incidents by making a PUT request
        put_resp = self.client().put(
            '/v2/user/put/incident/1',
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_two
            )
        self.assertEqual(put_resp.status_code, 200)
        get_resp = self.client().get(
            GET_URL,
            headers=dict(Authorization="Bearer " + token)
            )
        self.assertIn('Kilimani', str(get_resp.data))

    def test_user_can_delete_own_incident(self):
        """Test user can delete an existing incidents. (DELETE request)."""
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']

        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)
        # get the incidents in json
        results = json.loads(resp.data.decode())
        
        # delete the incidents we just created
        del_resp = self.client().delete(
            '/v2/user/del/incident/1',
            headers=dict(Authorization="Bearer " + token))
        self.assertEqual(del_resp.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get(GET_URL,
        headers=dict(Authorization="Bearer " + token)
        )
        self.assertEqual(result.status_code, 404)
    
    def test_user_cannot_delete_foreign_incidents(self):
        """test that foreign incidents cannot be deleted"""
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']

        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)
        
        self.register_user2()
        login_resp2 = self.login_user2()
        token2 = json.loads(login_resp2.data.decode())['user access token']

        resp2 = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token2),
            data=self.incident_two
            )
        self.assertEqual(resp2.status_code, 201)
        
        respdel = self.client().delete(
            '/v2/user/del/incident/2',
            headers=dict(Authorization="Bearer "+token))
        self.assertEqual(respdel.status_code, 404)

        respdel2 = self.client().delete(
            '/v2/user/del/incident/2',
            headers=dict(Authorization="Bearer "))
        self.assertEqual(respdel2.status_code, 401)

    def test_admin_cannot_delete_an_incident(self):
        """def"""
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']

        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)

        self.register_admin_user()
        login_resp2 = self.login_admin_user()
        token1 = json.loads(login_resp2.data.decode())['admin access token']

        respdel = self.client().delete(
            '/v2/user/del/incident/1',
            headers=dict(Authorization="Bearer "+token1))
        self.assertEqual(respdel.status_code, 401)

    def test_incidents_can_be_edited_by_admin(self):
        """Test API can edit an incident status. (PUT request)"""

        self.status ={"status":"Under investigation"}

        self.register_admin_user()
        self.register_user()

        result = self.login_user()
        token = json.loads(result.data.decode())['user access token']

        # first, we create a incidents by making a POST request

        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)
        # get the json with the incident
        results = json.loads(resp.data.decode())

        admin_login = self.login_admin_user()
        admin_token = json.loads(admin_login.data.decode())['admin access token']

        # then, we edit the created incidents by making a PUT request
        put_resp = self.client().put(
            '/v2/admin/put/incident/1',
            headers=dict(Authorization="Bearer " + admin_token),
            data=self.status
            )
        self.assertEqual(put_resp.status_code, 200)
        get_resp = self.client().get(
            GET_URL,
            headers=dict(Authorization="Bearer " + token)
            )
        self.assertIn('Under investigation', str(get_resp.data))

    def test_admin_can_get_all_incidents(self):
        """Test API can get all incidents (GET request)."""
        self.register_admin_user()
        self.register_user()
        login_resp = self.login_user()
        token = json.loads(login_resp.data.decode())['user access token']
        # create a incidents by making a POST request
        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)

        resp_2 = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_two
            )
        self.assertEqual(resp_2.status_code, 201)

        admin_login = self.login_admin_user()
        admin_token = json.loads(admin_login.data.decode())['admin access token']

        # get all the incidents that belong to the test user
        get_resp = self.client().get(
            '/v2/admin/get/incidents',
            headers=dict(Authorization="Bearer " + admin_token)
            )
        self.assertEqual(get_resp.status_code, 200)
        self.assertIn('Kilimani', str(get_resp.data))
        self.assertIn('Ngong', str(get_resp.data))

    def test_user_cannot_edit_non_draft_incident(self):
        """Test API can fetch a single incident (GET request)."""

        self.status ={"status":"Under investigation"}

        self.register_admin_user()
        self.register_user()

        login = self.login_user()
        token = json.loads(login.data.decode())['user access token']
        # create a incidents by making a POST request
        resp = self.client().post(
            POST_URL,
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_one
            )
        self.assertEqual(resp.status_code, 201)

        admin_login = self.login_admin_user()
        admin_token = json.loads(admin_login.data.decode())['admin access token']

        put_resp = self.client().put(
            '/v2/admin/put/incident/1',
            headers=dict(Authorization="Bearer " + admin_token),
            data=self.status
            )
        self.assertEqual(put_resp.status_code, 200)

        put_resp2 = self.client().put(
            '/v2/user/put/incident/1',
            headers=dict(Authorization="Bearer " + token),
            data=self.incident_two
            )
        self.assertEqual(put_resp2.status_code, 401)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()