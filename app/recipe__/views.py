from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core_app.models import Tag , Ingredient
from recipe__.serializers import TagSerializer , IngredientSerializer


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin
                 ):
    # a viewSet for the managing the tags
    # we're using ListModelMixin to make it doesn't allow any action but
    # retrieve, and the  CreateModelMixin to add creating feature

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    # the returned data of the call
    queryset = Tag.objects.all()

    # override the get func to return only the tags that
    # belongs to the user that made the request
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('name')

    # overriding the create func to
    # put the use with the serialized data
    def perform_create(self, serializer):
        # passing the requests user to the
        # serializer with the other data
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin
                 ):
    #  a viewSet for the managing the Ingredient
    # we're using ListModelMixin to make it doesn't allow any action but
    # retrieve, and the  CreateModelMixin to add creating feature

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = IngredientSerializer
    # the returned data of the call
    queryset = Ingredient.objects.all()

    # override the get func to return only the tags that
    # belongs to the user that made the request
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('name')

    # overriding the create func to
    # put the use with the serialized data
    def perform_create(self, serializer):
        # passing the requests user to the
        # serializer with the other data
        serializer.save(user=self.request.user)
