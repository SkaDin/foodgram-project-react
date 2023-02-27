from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from api.views import (
    RecipeViewSet,
    IngredientViewSet,
    IngredientInRecipeViewSet,
    TagViewSet,
    UserViewSet,
    FavoriteViewSet,
    ShoppingListViewSet
)

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'users/(?P<username>[\w.@+-]+)/',
    UserViewSet,
    basename='users'
)
router_v1.register(r'tags/(?P<pk>\d+)/', TagViewSet, basename='tags')
router_v1.register(
    r'recipes/(?P<pk>\d+)',
    RecipeViewSet,
    basename='recipes'
)
router_v1.register(
    r'recipes/(?P<pk>\d+)/shopping_list/',
    ShoppingListViewSet,
    basename='shopping_list'
)


urlpatterns = [
    
]
