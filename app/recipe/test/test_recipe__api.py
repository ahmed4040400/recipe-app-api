from django.contrib.auth import get_user_model
from core_app.models import Recipe, Tag, Ingredient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    return reverse("recipe:recipe-detail", args=[recipe_id])


def sample_tag(user, name="ahmed"):
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name="ahmed ingredient"):
    return Ingredient.objects.create(user=user, name=name)


# create a recipe sample
def sample_recipe(user, **params):
    defaults = {
        'title': "sample recipe",
        'time_minutes': 5,
        'price': 10.00

    }
    # update what it does is updating the default variable
    # with the data passed in params if added
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


# helper func for creating a simple user for testing
def create_user(email='ahmed@aa.com', password='as123sd', name='ahmed'):
    return get_user_model().objects.create_user(
        email=email,
        name=name,
        password=password
    )


class PublicRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """make sure that the recipe retrieve require authentication"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """test authorized access to recipe api """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        sample_recipe(user=self.user)
        sample_recipe(user=self.user, title='ahmed')

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('id')

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        """test that the Ingredient returned are for the authenticated user"""

        # create a different user to add a single Ingredient with
        user2 = create_user(email='ahmadded@ahmed.com')
        # making a Recipe with the different user
        sample_recipe(user=user2)
        # and then create a Recipe with the user that authed with the client
        sample_recipe(user=self.user, title='ahmed')
        # get the Recipe list with the authed client
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # make sure that we got 1 item in the data as expected
        self.assertEqual(len(res.data), 1)
        # and this 1 item is the authed users not the other ones
        self.assertEqual(res.data[0]['title'], 'ahmed')

    # test return more details when retrieving a specific recipe
    def test_view_recipe_detail(self):
        # create a recipe sample
        recipe = sample_recipe(user=self.user)
        # add a tag to it using the helper func sample_tag
        recipe.tags.add(sample_tag(user=self.user))
        # add a ingredient to it using the helper func sample_ingredient
        recipe.ingredients.add(sample_ingredient(user=self.user))
        # making request to retrieve specific recipe
        res = self.client.get(detail_url(recipe.id))
        # putting the returned recipe data in a serializer
        # that handles the detailed data
        serializer = RecipeDetailSerializer(recipe)
        # finally make sure the the serializer data
        # equals the returned data from the request
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """test creating recipe"""

        payload = {
            'title': "recipe title",
            'time_minutes': 40,
            'price': 52.00
        }
        # create a recipe and save the returned data to compare
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # get the recipe manually by filtering it from the db
        # using the id of the created one by the call
        recipe = Recipe.objects.get(id=res.data['id'])

        # loop through the payload keys
        # to make sure that the returned recipe from the call
        # equals the one we got it by filtering manually
        for key in payload.keys():
            # getattr(recipe, key) means "recipe.key"
            # this func helps when it comes to use attr from loops
            self.assertEqual(payload[key], getattr(recipe, key))

    # test creating a recipe with tags
    def test_create_recipe_with_tags(self):
        # creating the tags
        tag1 = sample_tag(user=self.user, name='ahmed')
        tag2 = sample_tag(user=self.user, name='ahmed2')
        # creating the payload with the tags
        payload = {
            'title': "recipe yummy",
            'tags': [tag1.id, tag2.id],
            'time_minutes': 40,
            'price': 52.00
        }
        # posting the payload to the url and get the response
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get the recipe manually by filtering it from the db
        # using the id of the created one by the call
        recipe = Recipe.objects.get(id=res.data['id'])
        # get the tags from the recipe we got manually to compare
        tags = recipe.tags.all()
        # make sure the the 2 tags we created are exists in the recipe
        self.assertEqual(tags.count(), 2)
        # make sure that the tags are the expected ones
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    # test creating a recipe with ingredients
    def test_create_recipe_with_ingredients(self):
        # create the ingredients
        ingredient1 = sample_ingredient(user=self.user, name='ahmed')
        ingredient2 = sample_ingredient(user=self.user, name='ahmed2')
        # creating the payload with the ingredients
        payload = {
            'title': "recipe yummy",
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 40,
            'price': 52.00
        }

        # posting the payload to the url and get the response
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get the recipe manually by filtering it from the db
        # using the id of the created one by the call
        recipe = Recipe.objects.get(id=res.data['id'])
        # get the ingredients from the recipe we got manually to compare
        ingredients = recipe.ingredients.all()
        # make sure the the 2 ingredient we created are exists in the recipe
        self.assertEqual(ingredients.count(), 2)
        # make sure that the ingredients are the expected ones
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_partial_update_recipe(self):
        # create a simple recipe
        recipe = sample_recipe(user=self.user)
        # add tag to it
        recipe.tags.add(sample_tag(user=self.user))
        # make another one and save it to patch with later
        newTag = sample_tag(user=self.user, name='newTag')
        # the payload we're gonna patch with containing the new tag and title
        payload = {
            'title': 'newTitle',
            'tags': [newTag.id]
        }
        # patching with the recipe id
        # getting the specific recipe url using the helper func detail_url()
        self.client.patch(detail_url(recipe.id), payload)
        # refresh the db to be able to assert
        recipe.refresh_from_db()

        # make sure that it's updated
        self.assertEqual(recipe.title, payload["title"])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(newTag, tags)

    def test_full_update_recipe(self):
        # create a simple recipe
        recipe = sample_recipe(user=self.user)
        # add tag to it to make sure it's gone after fully update (put)
        recipe.tags.add(sample_tag(user=self.user))
        # the payload the we're gonna update with
        payload = {
            'title': "recipe yummy1",
            'time_minutes': 40,
            'price': 52.00

        }
        # updating
        self.client.put(detail_url(recipe.id), payload)
        # refresh the db to be able to assert
        recipe.refresh_from_db()
        # make sure that everything is updated
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.time_minutes, payload["time_minutes"])
        self.assertEqual(recipe.price, payload["price"])
        # and the tag's gone
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)
