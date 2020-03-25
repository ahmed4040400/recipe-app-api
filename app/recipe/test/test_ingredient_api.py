from django.contrib.auth import get_user_model
from core_app.models import Ingredient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


# helper func for creating a simple user for testing
def create_user(email='ahmed@aa.com', password='as123sd', name='ahmed'):
    return get_user_model().objects.create_user(
        email=email,
        name=name,
        password=password
    )


class publicIngredientApiTest(TestCase):
    """test the publicly available Ingredients api """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login required to access the endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class privateIngredientApiTest(TestCase):
    """test Ingredient can be retrieved by authorized users"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_Ingredient(self):
        # creating some Ingredient to test retrieving them
        Ingredient.objects.create(user=self.user, name='ahmed')
        Ingredient.objects.create(user=self.user, name='amr')
        # getting the Ingredient with client
        res = self.client.get(INGREDIENT_URL)
        # getting them directly from the db to compare them
        # with the ones we got from the http call
        # and order them by name just like return value of http call
        tags = Ingredient.objects.all().order_by('name')
        # validate the data we got from the db to simulate
        # the http call to make a clean compare
        # because the http call will serialize
        # the data before sending it
        serializer = IngredientSerializer(tags, many=True)
        # make sure we get a status code 200_ok
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # comparing the returned data with the directly retrieved one
        self.assertEqual(res.data, serializer.data)

    def test_Ingredient_limited_to_user(self):
        """test that the Ingredient returned are for the authenticated user"""

        # create a different user to add a single Ingredient with
        user2 = create_user(email='ahmed@ahmed.com')
        # making a Ingredient with the different user
        Ingredient.objects.create(user=user2, name='whatever')
        # and then create a Ingredient with the user that authed with the client
        Ingredient.objects.create(user=self.user, name='ahmed')
        # get the Ingredient list with the authed client
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # make sure that we got 1 item in the data as expected
        self.assertEqual(len(res.data), 1)
        # and this 1 item is the authed user not the other one
        self.assertEqual(res.data[0]['name'], 'ahmed')

    def test_create_Ingredient_successful(self):
        """test creating a new tag"""

        payload = {'name': 'test Ingredient'}
        res = self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_Ingredient_invalid_name(self):
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
