from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import (
    GenericViewSet,
    ReadOnlyModelViewSet,
)
from api.serializers import (
    IngredientSerializer,
    SmallRecipeSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    SubscribtionSerializer,
    TagSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscribers


User = get_user_model()


#class CreateRetrieveDestroyViewSet(
#    CreateModelMixin,
#    RetrieveModelMixin,
#    DestroyModelMixin,
#    GenericViewSet
#):
#    """Базовый класс вьюсета."""
#    pass


class UsersSubscriptionsViewSet(GenericViewSet):
    """Вьюсет для пользователей: подписки/отписки, список подписок. """
    queryset = User.objects.all()
    serializer_class = SubscribtionSerializer



class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для работы с тэгами."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

