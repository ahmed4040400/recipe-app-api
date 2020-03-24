from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core_app.models import Tag , Ingredient
from recipe__.serializers import TagSerializer , IngredientSerializer


# a viewSet for the managing the tags and Ingredient
# we're using ListModelMixin to make it doesn't allow any action but
# retrieve, and the  CreateModelMixin to add creating feature
class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # override the get func to return only the attr that
    # belongs to the user that made the request
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('id')

    # overriding the create func to
    # put the use with the serialized data
    def perform_create(self, serializer):
        # passing the requests user to the
        # serializer with the other data
        serializer.save(user=self.request.user)


# a viewSet for the managing the tags
# inherits from the user base recipe attr class
class TagViewSet(BaseRecipeAttrViewSet):
    serializer_class = TagSerializer
    # the returned data of the call
    queryset = Tag.objects.all()


# a viewSet for the managing the Ingredient
# inherits from the user base recipe attr class
class IngredientViewSet(BaseRecipeAttrViewSet):
    serializer_class = IngredientSerializer
    # the returned data of the call
    queryset = Ingredient.objects.all()

