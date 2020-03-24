from django.contrib.auth import get_user_model
from core_app.models import Tag
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe__.serializers import TagSerializer

# because we're using viewSet for the tag model
# so the url for getting the object has to be "tag-list"

TAGS_URL = reverse('recipe__:tag-list')


# helper func for creating a simple user for testing
def create_user(email='ahmed@aa.com', password='as123sd', name='ahmed'):
    return get_user_model().objects.create_user(
        email=email,
        name=name,
        password=password
    )


class PublicTagsApiTest(TestCase):
    """test the publicly available tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving tags"""

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """test authorized user ability for tags api"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        # creating some tags to test retrieving them
        Tag.objects.create(user=self.user, name='ahmed')
        Tag.objects.create(user=self.user, name='amr')
        # getting the tags with client
        res = self.client.get(TAGS_URL)
        # getting them directly from the db to compare them
        # with the ones we got from the http call
        # and order them by name just like return value of http call
        tags = Tag.objects.all().order_by('name')
        # validate the data we got from the db to simulate
        # the http call to make a clean compare
        # because the http call will serialize
        # the data before sending it
        serializer = TagSerializer(tags, many=True)
        # make sure we get a status code 200_ok
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # comparing the returned data with the directly retrieved one
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_to_user(self):
        """test that the tags returned are for the authenticated user"""

        # create a different user to add a single tag with
        user2 = create_user(email='ahmed@ahmed.com')
        # making a tag with the different user
        Tag.objects.create(user=user2, name='whatever')
        # and then create a tag with the user that authed with the client
        tag = Tag.objects.create(user=self.user, name='ahmed')
        # get the tags list with the authed client
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # make sure that we got 1 item in the data
        self.assertEqual(len(res.data), 1)
        # and this 1 item is the authed user not the other one
        self.assertEqual(res.data[0]['name'], 'ahmed')

    def test_create_tags_successful(self):
        """test creating a new tag"""

        payload = {'name': 'test tag'}
        res = self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_tag_invalid_name(self):
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
