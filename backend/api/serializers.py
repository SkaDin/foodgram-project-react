import base64

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    ImageField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)
from recipes.models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag
)

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )

class UserBaseSerializer(UserSerializer):
    """Сериализатор для работы с моделью пользователя."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        feilds = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            user = get_object_or_404(
                User,
                username=self.context['request'].user
            )
            return user.follower.filter(author=obj.id).exists()
        return False    


class IngredientSerializer(ModelSerializer):
    """Сериализатор для работы с моделью ингредиентов."""
    class Meta:
        model = Ingredient
        fileds = (
            'id',
            'name',
            'measurement_unit'
        )

class TagSerializer(ModelSerializer):
    """Сериализатор для работы с моделью тегов."""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientRecipeSerializer(ModelSerializer):
    """
    Сериализатор для работы со связанной таблицей рецептов 
    и ингредиентов.
    """
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = CharField(
        source='ingredient.name',
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

class Base64ImageField(ImageField):
    """
    Создание кастомного типа поля для картинки
    и переопределение метода "to_internal_value"
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)
    

class RecipeSerializer(ModelSerializer):
    """Сериализатор для работы с моделью рецептов (retriev/list)."""
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(
        source='recipe_ingredients',
        many=True
    )
    author = UserBaseSerializer(
        read_only=True,
        default=CurrentUserDefault()
    )
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_farorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

        def get_is_favorited(self, obj):
            if self.context['request'].user.is_authenticated:
                user = get_object_or_404(
                    User,
                    username=self.context['request'].user
                )
                return user.favorited.filter(recipe=obj.id).exists()
            return False
        
        def get_is_in_shopping_cart(self, obj):
            if self.context['request'].user.is_authenticated:
                user = get_object_or_404(
                    User,
                    username=self.context['request'].user
                )
                return user.shopping.cart.filter(recipe=obj.id).exists()
            return False
        
class RecipeCreateSerializer(RecipeSerializer):
    """Сериалазатор для работы с моделью рецептов(create)."""
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    class Meta:
        model = Tag
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
            'cooking_time'
        )
    @staticmethod
    def save_ingredients(recipe, ingredients):
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            current_amount = ingredient['amount']
            ingredients_list.append(
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=current_ingredient,
                    amount=current_amount
                )            
            )
        IngredientRecipe.objects.bulk_create(ingredients_list)

    def create(self, validated_data):
        author = self.context['request'].user
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.add(*tags)
        self.save_ingredients(recipe, ingredients)
        return recipe
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('iamge', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        instance.ingredients.clear()
        recipe = instance
        self.save_ingredients(recipe, ingredients)
        instance.save()
        return instance
    

class SmallRecipeSerializer(RecipeSerializer):
    """Сериализатор для отображения рецептов в подписках."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

class SubscribtionSerializer(UserBaseSerializer):
    """Сериализатор для работы с моделью подписчиков."""
    recipes = SmallRecipeSerializer(read_only=True, many=True)
    recipes_count = IntegerField(
        source='recipes.count',
        read_only=True
    )

    class Meta:
        model = User
        fileds = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipe',
            'recipe_count',
        )