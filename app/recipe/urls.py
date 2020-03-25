from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views


# we use routers cause we're using a ViewSet for the this views
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)
app_name = 'recipe'
urlpatterns = [
    path('', include(router.urls))
]

