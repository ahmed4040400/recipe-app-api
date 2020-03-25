from rest_framework import serializers
from core_app import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):

    # PrimaryKeyRelatedField():
    # is for defining the fields that's related to a
    # whole different model and serializer
    # to let this serializer know how to validate
    # we use it if we wanna get only the objects id
    # otherwise we use the objects serializer
    ingredients = serializers.PrimaryKeyRelatedField(
        # means that we can have more than
        # one object for on recipe object
        many=True,
        # the model objects that we're gonna query
        queryset=models.Ingredient.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        # means that we can have more than
        # one object for on recipe object
        many=True,
        # the model objects that we're gonna query
        queryset=models.Tag.objects.all()
    )

    class Meta:
        model = models.Recipe
        fields = (
            'id', 'title', 'time_minutes', 'price',
            'tags', 'ingredients', 'link'
        )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):

    # we inherit every thing from RecipeSerializer()
    # and add few things
    # this time we use the ingredients and tags serializers
    # to get more details about them in the returned data

    ingredients = IngredientSerializer(
        # means that we can have more than
        # one object for on recipe object
        many=True,
        # so no one can edit the object inside the recipe
        read_only=True
    )

    tags = TagSerializer(
        # means that we can have more than
        # one object for on recipe object
        many=True,
        # so no one can edit the object inside the recipe
        read_only=True
    )
