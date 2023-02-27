from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from recipes.models import (
    Recipe,
    Ingredient,
    Tag,
    IngredientInRecipe,
    Favorite,
    ShoppingList,
)

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__',)


class RecipeSerializer(ModelSerializer):  
    class Meta:
        model = Recipe
        fields = ('__all__',)


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__',)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__',)


class IngredientInRecipeSerializer(ModelSerializer):
    class Meta:
        model = IngredientInRecipe
        feilds = ('__all__',)


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('__all__',)


class ShoppingListSerializer(ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('__all__',)
