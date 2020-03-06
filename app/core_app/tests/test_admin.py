from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    # setUP() is a callback that get called before testing anything
    def setUp(self):
        # putting the client variable in a bigger scope
        self.client = Client()
        # creating the admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email="ahaga@gmail.com",
            password="tes5674asf65",
            name="amr"
        )
        # login with the admin user using the clint var
        self.client.force_login(self.admin_user)
        # creating a normal user
        self.user = get_user_model().objects.create_user(
            email="ahhh@agoogle.com",
            password="123123asd3213",
            name='razan'
        )

    # the testing method
    def test_users_listed(self):
        # creating the url using the reverse()
        # and adding the path we wanna match
        url = reverse('admin:core_app_user_changelist')
        # getting the desired items using the get(url)
        # by the logged in superuser
        res = self.client.get(url)
        # test that it returns the users name
        self.assertContains(res, self.user.name)
        # test that it returns the users email
        self.assertContains(res, self.user.email)

    def test_change_page(self):
        url = reverse('admin:core_app_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_creat_user_page(self):
        url = reverse('admin:core_app_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
