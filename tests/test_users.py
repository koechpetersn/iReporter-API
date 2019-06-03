# /tests/test_auth.py

import unittest
import json
from app import create_app, db


class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(configure="testing")
        # initialize the test client
        self.client = self.app.test_client
        #Sample test user data
        self.user_data_1 = {
            'email': 'test@example.com',
            'password': 'test_password'
        }
        self.user_data_2 = {
            'email':'example@admin',
            'password' : 'passpass'
        }

        with self.app.app_context():
            db.create_all()

    def register_an_admin_user(
        self, 
        email="user@admin", 
        password="pass1234"):

        """This helper method helps register an admin user."""
        
        admin_data = {
            'email': email,
            'password': password
        }
        return self.client().post(
            '/v2/admin/signup',
            data=admin_data
        )

    def login_admin(
        self,
        email="user@admin",
        password="pass1234"):

        """This helper method helps log in an admin user."""

        admin_data = {
            'email': email,
            'password': password
        }
        return self.client().post(
            '/v2/admin/signin',
            data=admin_data
        )

    def test_registration(self):
        """Test user registration works correcty."""
        resp = self.client().post(
            '/v2/user/signup',
            data=self.user_data_1
        )
        # get the results returned in json format
        result = json.loads(resp.data.decode())
        # assert that the request contains a success message
        self.assertEqual(result['message'],
        "You registered successfully. Please log in.")
        self.assertEqual(resp.status_code, 201)

    def test_user_cannot_register_twice(self):
        """Test that a user cannot be registered twice."""
        resp = self.client().post(
            '/v2/user/signup',
            data=self.user_data_1)

        self.assertEqual(resp.status_code, 201)
        second_resp = self.client().post(
            '/v2/user/signup',
            data=self.user_data_1
        )
        self.assertEqual(second_resp.status_code, 202)
        # get the results returned in json format
        result = json.loads(second_resp.data.decode())
        self.assertEqual(
            result['message'],
            "User already exists. Please login."
            )

    def test_user_login(self):
        """Test registered user can login."""
        resp = self.client().post(
            '/v2/user/signup',
            data=self.user_data_1
        )
        self.assertEqual(resp.status_code, 201)
        login_resp = self.client().post(
            '/v2/user/signin',
            data=self.user_data_1
            )

        # get the results in json format
        result = json.loads(login_resp.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], "You logged in successfully.")
        # Assert that the status code is equal to 200
        self.assertEqual(login_resp.status_code, 200)
        self.assertTrue(result['user access token'])

    def test_admin_user_can_login(self):
        """Test registered admin user can login."""
        resp = self.client().post(
            '/v2/admin/signup',
            data=self.user_data_1
            )
        self.assertEqual(resp.status_code, 201)
        login_resp = self.client().post(
            '/v2/admin/signin',
            data=self.user_data_1
            )

        # get the results in json format
        result = json.loads(login_resp.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], "You logged in successfully.")
        # Assert that the status code is equal to 200
        self.assertEqual(login_resp.status_code, 200)
        self.assertTrue(result['admin access token'])

    def test_alien_inability_to_login(self):
        """Test non registered users cannot login."""
        # send a POST request to user login without registration
        resp = self.client().post(
            '/v2/user/signin',
            data=self.user_data_1
            )
        # get the result in json
        result = json.loads(resp.data.decode())

        # assert that this response must contain an error message 
        # and an error status code 401(Unauthorized)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            result['message'],
            "Invalid email or password, Please try again"
            )

    def test_alien_inability_to_login_as_admin(self):
        """Test non registered users cannot login."""
        # send a POST request to admin login without registration
        resp = self.client().post(
            '/v2/admin/signin',
            data=self.user_data_1
            )
        # get the result in json
        result = json.loads(resp.data.decode())

        # assert that this response must contain an error message 
        # and an error status code 401(Unauthorized)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            result['message'],
            "Invalid email or password, Please try again"
            )

    def test_non_admin_user_inability_to_login_as_admin(self):
        """Test that a non admin user cannot be logged in as an admin."""
        resp = self.client().post(
            '/v2/user/signup',
            data=self.user_data_1)
        self.assertEqual(resp.status_code, 201)
        second_resp = self.client().post(
            '/v2/admin/signin',
            data=self.user_data_1
            )
        self.assertEqual(second_resp.status_code, 401)
        # get the results returned in json format
        result = json.loads(second_resp.data.decode())
        self.assertEqual(
            result['message'],
            "Not admin user! Please login as a normal user"
            )

    def test_admin_user_can_delete_user(self):
        """Test an admin can deregister a user."""
        resp = self.client().post(
            '/v2/user/signup',
            data=self.user_data_1
            )
        self.assertEqual(resp.status_code, 201)

        self.register_an_admin_user()
        result = self.login_admin()
        token = json.loads(result.data.decode())['admin access token']

        
        login_resp = self.client().delete('/v2/admin/del/user/1',
        headers=dict(Authorization="Bearer " + token))

        # get the results in json format
        result = json.loads(login_resp.data.decode())
        # Test that the response contains success message
        self.assertEqual(
            result['message'],
            "User successfully deregistered"
            )
        # Assert that the status code is equal to 200
        self.assertEqual(login_resp.status_code, 200)

    def test_admin_user_can_get_a_specific_user(self):
        """Test an admin can fetch a user."""
        resp = self.client().post(
            '/v2/user/signup',
            data=self.user_data_1
            )
        self.assertEqual(resp.status_code, 201)

        self.register_an_admin_user()
        result = self.login_admin()
        token = json.loads(result.data.decode())['admin access token']
        login_resp = self.client().get(
            '/v2/admin/get/user/1',
            headers=dict(Authorization="Bearer " + token)
            )
        # get the results in json format
        result = json.loads(login_resp.data.decode())
        ress = result["message"]
        resss = ress[0]
        ressss = resss["id"]
        # Test that the response contains success message
        self.assertEqual(1,ressss)
        # self.assertEqual(result['message'], "User successfully deregistered")
        self.assertEqual(login_resp.status_code, 200)

    def test_admin_user_can_get_all_users(self):
        """Test an admin can fetch all users."""
        resp = self.client().post(
            '/v2/user/signup',
            data=self.user_data_1
            )
        resp_2 = self.client().post(
            '/v2/user/signup',
            data=self.user_data_2
            )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp_2.status_code, 201)
        self.register_an_admin_user()
        result = self.login_admin()
        token = json.loads(result.data.decode())['admin access token']
        login_resp = self.client().get(
            '/v2/admin/get/users',
            headers=dict(Authorization="Bearer " + token)
            )
        # get the results in json format
        result = json.loads(login_resp.data.decode())
        ress = result["all registered users"]
        resss = ress[0]
        ressss = resss["id"]
        # Test that the response contains success message
        self.assertEqual(1,ressss)
        # self.assertEqual(result['message'], "User successfully deregistered")
        self.assertEqual(login_resp.status_code, 200)
        
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()

    


