"""
generics: punch of ApiViews
that gives you shortcuts that map closely to your database models.
Adds commonly required behavior for standard list and detail views.
Gives you some attributes like, the serializer_class,
also gives pagination_class, filter_backend, etc
"""
from rest_framework import generics, authentication, permissions
from user import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):

    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = serializers.AuthTokenSerializer
    
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):

    serializer_class = serializers.UserSerializer
    # the authentication type in this case it's a TokenAuthentication
    authentication_classes = (authentication.TokenAuthentication,)
    # the user can't use the view if not authorized
    permission_classes = (permissions.IsAuthenticated,)

    # overriding the get method to return just the individual user
    # that's making the request
    def get_object(self):
        return self.request.user
