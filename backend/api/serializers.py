import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer,
    ImageField,
    CharField,
    PrimaryKeyRelatedField,
    SerializerMethodField
)
from rest_framework.exceptions import ValidationError
from recipes.models import (
    Favorite, 
    Ingredient, 
    Recipe, 
    IngredientRecipe,
    ShoppingCart, 
    Tag
)
from users.models import Subscribers, User
from foodgram.settings import LIMIT_VIEW_RECIPE


class UsersCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для обработки запросов на создание пользователя.
    Валидирует создание пользователя с юзернеймом 'me'.
    """
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Невозможно создать пользователя с таким именем!'
            )
        return value


class UserInfoSerializer(UserSerializer):
    """Сериализатор для отображения информации о пользователе."""
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribers.objects.filter(
            user=user,
            author=obj.id).exists()


class FollowSerializer(UserInfoSerializer):
    """Сериализатор для добавления/удаления подписки, просмотра подписок."""
    recipes = SerializerMethodField(read_only=True)
    recipes_count = SerializerMethodField(read_only=True)

    class Meta(UserInfoSerializer.Meta):
        fields = UserInfoSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, object):
        request = self.context.get('request')
        context = {'request': request}
        recipe_limit = request.query_params.get('recipes_limit')
        queryset = object.recipes.all()[:LIMIT_VIEW_RECIPE]
        if recipe_limit:
            queryset = queryset[:int(recipe_limit)]
        return RecipeInfoSerializer(
            queryset,
            context=context,
            many=True).data

    def get_recipes_count(self, object):
        return object.recipes.count()
    

class Base64ImageField(ImageField):
    """Кастомное поле для кодирования изображения в base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name='temp.' + ext
            )
        return super().to_internal_value(data)


class TagSerializer(ModelSerializer):
    """Сериализатор для работы с тегами."""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(ModelSerializer):
    """Сериализатор для работы с ингредиентами."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class RecipeIngredientSerializer(ModelSerializer):
    """Сериализатор для подробного описания ингредиентов в рецепте."""
    name = CharField(
        source='ingredient.name',
        read_only=True
    )
    id = PrimaryKeyRelatedField(
        source='ingredient.id',
        read_only=True
    )
    measurement_unit = CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class AddIngredientSerializer(ModelSerializer):
    """Сериализатор для добавления ингредиента при создании рецепта."""
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount'
        )


class RecipeSerializer(ModelSerializer):
    """
    Сериализатор создания рецепта.
    Валидирует ингредиенты ответ возвращает GetRecipeSerializer.
    """
    author = UserInfoSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = AddIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        list_ingr = [item['ingredient'] for item in data['ingredients']]
        all_ingredients, distinct_ingredients = (
            len(list_ingr), len(set(list_ingr)))

        if all_ingredients != distinct_ingredients:
            raise ValidationError(
                {'error': 'Ингредиенты должны быть уникальными'}
            )
        return data

    def get_ingredients(self, recipe, ingredients):
        IngredientRecipe.objects.bulk_create(
            IngredientRecipe(
                recipe=recipe,
                ingredient=ingredient.get('ingredient'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients)

    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=user,
            **validated_data
        )
        recipe.tags.set(tags)
        self.get_ingredients(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        IngredientRecipe.objects.filter(recipe=instance).delete()

        instance.tags.set(tags)
        self.get_ingredients(instance, ingredients)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return GetRecipeSerializer(instance, context=context).data


class GetRecipeSerializer(ModelSerializer):
    """Сериализатор для отображения полной информации о рецепте."""
    tags = TagSerializer(many=True)
    author = UserInfoSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        read_only=True,
        many=True,
        source='recipe_ingredient'
    )
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            try:
                obj.favorites.get(user=user)
                return True
            except Favorite.DoesNotExist:
                return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            try:
                obj.shopping_carts.get(user=user)
                return True
            except ShoppingCart.DoesNotExist:
                return False


class FavoriteSerializer(ModelSerializer):
    """Сериализатор добавления/удаления рецепта в избранное."""
    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        user, recipe = data['user'], data.get('recipe')
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(
                {'error': 'Этот рецепт уже добавлен'}
            )
        return data

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeInfoSerializer(instance.recipe, context=context).data


class ShoppingCartSerializer(FavoriteSerializer):
    """Сериализатор добавления/удаления рецепта в список покупок."""
    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart


class RecipeInfoSerializer(ModelSerializer):
    """Сериализатор для отображения краткой информации о рецепте."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
