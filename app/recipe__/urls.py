from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe__ import views


# we use routers cause we're using a ViewSet for the tags view
router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe__'
urlpatterns = [
    path('', include(router.urls))
]

