# # tests/test_app.py
# import unittest
# import os
# import json
# from app import create_app


# class IncidentTestCase(unittest.TestCase):
#     """This class represents the incident test case"""

#     def setUp(self):
#         """Define test variables and initialize app."""
#         self.app = create_app(configure="testing")
#         self.client = self.app.test_client()
#         self.incident = {
#             'media': 'video',
#             'comment': 'bbf',
#             'location': 'bchsbc'
#         }

#         # binds the app to the current context
#         with self.app.app_context():
#             # create all tables
#             db.create_all()

#     def register_user(self, email="user@test.com", password="test1234",username="mose"):
#         """This helper method helps register a test user."""
#         user_data = {
#             'email': email,
#             "username":username,
#             'password': password
#         }
#         return self.client().post('/auth/register', data=user_data)

#     def login_user(self, email="user@test.com", password="test1234"):
#         """This helper method helps log in a test user."""
#         user_data = {
#             'email': email,
#             'password': password
#         }
#         return self.client().post('/auth/login', data=user_data)

#     def test_incident_creation(self):
#         """Test API can create a bucketlist (POST request)"""
#         # register a test user, then log them in
#         self.register_user()
#         # obtain the access token
#         result = self.login_user()
#         access_token = json.loads(result.data.decode())['access_token']
#         # ensure the request has an authorization header set with the access token in it
#         res = self.client().post('/incidents/',headers=dict(Authorization="Bearer " + access_token), data=self.incident)
#         self.assertEqual(res.status_code, 201)
#         self.assertIn('bbf', str(res.data))

#     def test_api_can_get_all_incidents(self):
#         """Test API can get a bucketlist (GET request)."""
#         self.register_user()
#         result = self.login_user()
#         access_token = json.loads(result.data.decode())['access_token']
#         # create a bucketlist by making a POST request
#         res = self.client().post('/incidents/',headers=dict(Authorization="Bearer " + access_token), data=self.incident)
#         self.assertEqual(res.status_code, 201)
#         # get all the bucketlists that belong to the test user by making a GET request
#         res = self.client().get('/incidents/',headers=dict(Authorization="Bearer " + access_token))
#         self.assertEqual(res.status_code, 200)
#         self.assertIn('video', str(res.data))

#     def test_api_can_get_incidents_by_id(self):
#         """Test API can get a single bucketlist by using it's id."""
#         self.register_user()
#         result = self.login_user()
#         access_token = json.loads(result.data.decode())['access_token']

#         rv = self.client().post('/incidents/',headers=dict(Authorization="Bearer " + access_token), data=self.incident)
#         self.assertEqual(rv.status_code, 201)
#         # get the response data in json format
#         result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
#         result = self.client().get(
#             '/incidents/{}'.format(result_in_json['id']),headers=dict(Authorization="Bearer " + access_token))
#         # assert that the bucketlist is actually returned given its ID
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('redflag', str(result.data))

#     def test_incidents_can_be_edited(self):
#         """Test API can edit an existing bucketlist. (PUT request)"""
#         self.register_user()
#         result = self.login_user()
#         access_token = json.loads(result.data.decode())['access_token']

#         # first, we create a bucketlist by making a POST request

#         rv = self.client().post(
#             '/incidents/',
#             headers=dict(Authorization="Bearer " + access_token),
#             data={
#                 'media':'gg',
#                 'location':'embu',
#                 'comment':'nada'
#             })
#         self.assertEqual(rv.status_code, 201)
#         # get the json with the bucketlistttttttttttttttttttttttttttttttttttttt
#         results = json.loads(rv.data.decode())

#         # then, we edit the created bucketlist by making a PUT request
#         rv = self.client().put(
#             '/incidents/1',
#             headers=dict(Authorization="Bearer " + access_token),
#             data={
#                 'media':'nogg',
#                 'location':'aembu',
#                 'comment':'dada'
#             })
#         self.assertEqual(rv.status_code, 200)
#         results = self.client().get('/incidents/1',headers=dict(Authorization="Bearer " + access_token))
#         self.assertIn('nogg', str(results.data))

#     def test_incident_deletion(self):
#         """Test API can delete an existing bucketlist. (DELETE request)."""
#         self.register_user()
#         result = self.login_user()
#         access_token = json.loads(result.data.decode())['access_token']

#         rv = self.client().post(
#             '/incidents/',
#             headers=dict(Authorization="Bearer " + access_token),
#             data={
#                 'media':'nogg',
#                 'location':'aembu',
#                 'comment':'dada'
#             })
#         self.assertEqual(rv.status_code, 201)
#         # get the bucketlist in json
#         results = json.loads(rv.data.decode())
        
#         # delete the bucketlist we just created
#         res = self.client().delete('/incidents/1',headers=dict(Authorization="Bearer " + access_token))
#         self.assertEqual(res.status_code, 200)
#         # Test to see if it exists, should return a 404
#         result = self.client().get('/incidents/1',headers=dict(Authorization="Bearer " + access_token))
#         self.assertEqual(result.status_code, 404)

#     def tearDown(self):
#         """teardown all initialized variables."""
#         with self.app.app_context():
#             # drop all tables
#             db.session.remove()
#             db.drop_all()
# # Make the tests conveniently executable
# # if __name__ == "__main__":
# #     unittest.main()