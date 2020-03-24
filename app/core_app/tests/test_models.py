from django.test import TestCase
# for getting the model that handles the auth stuff
# now we could've used the the model name
# but django recommend using this class
from django.contrib.auth import get_user_model

from core_app import models


# this is a unit test code that test
# the custom users model that takes email
# instead of username
# we test it using the assertEqual()
# that takes 2 values if the're equal it return ok
# if not it returns an error message

def sample_user(email='ahmed@ahmed.com', password='asd123313', name='ahmed'):
    """create simple user"""

    return get_user_model().objects.create_user(
        email=email,
        password=password,
        name=name
    )


class ModelTest(TestCase):
    # the test method should start with the name test
    def test_create_user_with_email_successful(self):
        """test creating a new user with email is successful"""
        email = "test@gmail.com"
        password = "test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name='ahmed2'
        )

        self.assertEqual(user.email, email)
        # assertTrue() returns ok if the value returns true
        # and vice versa
        self.assertTrue(user.check_password(password))

    def test_create_new_user_email_normalized(self):
        user = get_user_model().objects.create_user(
            email="ahmed@GMAIL.COM",
            password="asfasdf123",
            name="ahmed",
        )

        self.assertEqual(user.email, "ahmed@gmail.com")

    def test_create_user_with_invalid_email(self):
        """assertRaises() listens for error if we got error
            the test passes otherwise it fails
            the with is for adding the code that is going to
            be tested
        """
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(None, "123321")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="ahmed@gmail.com",
            password='213sadf1',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test the tag string representation
           which is the return value of the __str__() in the model
        """

        tag = models.Tag.objects.create(
            user=sample_user(),
            name='ahmed',
        )

        self.assertEqual(str(tag), tag.name)
