from rest_framework.viewsets import ModelViewSet
from recipes.models import (
    Recipe,
    Ingredient,
    Tag,
    IngredientInRecipe,
    Favorite,
    ShoppingList,
)
from django.contrib.auth import get_user_model
from api.serializers import (
    RecipeSerializer,
    IngredientSerializer,
    IngredientInRecipeSerializer,
    TagSerializer,
    ShoppingListSerializer,
    FavoriteSerializer,
    UserSerializer
)


User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serialier_class = IngredientSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientInRecipeViewSet(ModelViewSet):
    queryset = IngredientInRecipe
    serializer_class = IngredientInRecipeSerializer

class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class ShoppingListViewSet(ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
