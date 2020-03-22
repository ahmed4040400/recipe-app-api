from django.test import TestCase
from django.contrib.auth import get_user_model
# for generating the the request url
from django.urls import reverse
# for making virtual api calls
from rest_framework.test import APIClient
# just contains variable contains the status code
# to make the code cleaner
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


# for testing creating user already exist
def create_user(**params):
    user = get_user_model().objects.create_user(**params)
    return user


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    # test creating a valid user using and password safety
    def test_create_valid_user_success(self):
        payload = {
            'email': "ahmed4664@gmail.com",
            'name': 'ahmed555',
            'password': 'Afsf56464'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    # test creating a user that already exist fails
    def test_user_exists(self):
        payload = {
            'email': "ahmed123@gmail.com",
            'name': 'ahmed5545',
            'password': 'Afsf56464'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # make sure that creating a user with short pass fails
    def test_password_short(self):

        payload = {
            'email': "ahmed123@gmail.com",
            'name': 'ahmed5545',
            'password': 's'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # getting the user then make sure that it's not exist
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)
    # test the token created successful with valid email & password
    def test_create_token_for_user(self):
        payload = {'email': 'test@tesr.com', 'password': "asf1432"}
        create_payload = {
            'email': 'test@tesr.com',
            'name': 'ahmed',
            'password': "asf1432"
        }

        create_user(**create_payload)
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    # test creating a token with invalid email return 400 status code
    def test_create_token_invalid_credentials(self):
        payload = {'email': 'ahmed@gmail.com', 'password': "asf1432"}
        create_payload = {
            'email': 'test@tesr.com',
            'name': 'ahmed',
            'password': "asf1432"
        }

        create_user(**create_payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # test token's not created if there is no user
    def test_create_token_no_user(self):
        payload = {'email': 'ahmed@gmail.com', 'password': "asf1432"}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # test not creating token if there is messing fields
    def test_create_token_messing_field(self):
        payload = {'email': 'ahmed', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # testing retrieving a user without being unauthorized
    #and make sure it doesn't return the user
    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):

    def setUp(self):
        self.user = create_user(
            email='ahmed@ahmed.com',
            name='ahmed',
            password='Afff123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_authorized(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {
            'name': "newName",
            'password': "newPassword0123"
        }

        res = self.client.patch(ME_URL, payload)
        # refreshing the db to make sure it up to date after patched
        self.user.refresh_from_db()

        self.assertEqual(res.data['name'], payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
