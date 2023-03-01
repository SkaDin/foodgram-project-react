from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
    FavoriteViewSet,
    ShoppingListViewSet
)

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'resipes', ShoppingListViewSet, basename='shopping_list')
router.register(r'recipes', FavoriteViewSet, basename='favorites')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls))
]
