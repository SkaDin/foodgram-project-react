from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    FavoriteSerializer,
    ShoppingListSerializer
)
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    ShoppingList
)

User = get_user_model()


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = ()
    authentication_classes = ()


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = ()
    authentication_classes = ()


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = ()
    authentication_classes = ()


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = ()
    authentication_classes = ()


class ShoppingListViewSet(ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    permission_classes = ()
    authentication_classes = ()