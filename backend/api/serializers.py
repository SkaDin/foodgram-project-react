from rest_framework.serializers import ModelSerializer

from django.contrib.auth import get_user_model
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    ShoppingList,
)
from users.models import Subscribers


User = get_user_model()


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class ShoppingListSerializer(ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = '__all__'