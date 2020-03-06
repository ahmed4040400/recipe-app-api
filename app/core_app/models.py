from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):

    # create a normal user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("the user must has an email")
        # the **extra_field field is if i ever wanted to add
        # some extra information to the user
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name='admin', **extra_fields):
        user = self.create_user(
            email=email,
            password=password,
            name=name,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=200, unique=True)
    name = models.CharField(max_length=100, unique=False)
    # has admin permissions
    is_staff = models.BooleanField(default=False)
    # the account is activated
    is_active = models.BooleanField(default=True)
    # the manager of the users
    objects = UserManager()
    # the field that's gonna take the username field place
    USERNAME_FIELD = 'email'
    # adding some extra required fields
    REQUIRED_FIELDS = ['name']
