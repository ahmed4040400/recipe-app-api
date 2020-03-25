from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings


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


class Tag(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(
        # telling which model we're gonna connect with
        settings.AUTH_USER_MODEL,
        # if the connected model object got deleted
        # we delete this object as well
        on_delete=models.CASCADE

    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(
        # telling which model we're gonna connect with
        settings.AUTH_USER_MODEL,
        # if the connected model object got deleted
        # we delete this object as well
        on_delete=models.CASCADE

    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    title = models.CharField(max_length=150)
    user = user = models.ForeignKey(
        # telling which model we're gonna connect with
        settings.AUTH_USER_MODEL,
        # if the connected model object got deleted
        # we delete this object as well
        on_delete=models.CASCADE
    )

    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # param blank=True to make this field optional
    link = models.CharField(max_length=255, blank=True)

    """ManyToManyField() is like ForeignKey() 
       but it allows to have more than on object for the field
       on the opposite of the ForeignKey() which allows only 
       one object for one fields
    """
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
