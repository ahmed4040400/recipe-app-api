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


# for testing creating user already exist
def create_user(**params):
    user = get_user_model().objects.create_user(**params)


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

        create_user(payload)
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
        # getting the user then make sure that it exists
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertTrue(user_exists)

