from django.contrib.auth import get_user_model
from django.db import models
from users.models import User
from recipes.validators import validator_coocing_time, validator_amount

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        default='#ffffff'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True
    )
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.slug



class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=20
    )

    class Meta:
        ordering = ['name']
        verbose_name='Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
            fields=['name', 'measurement_unit'],
            name='unique_name_measurement_unit'
            )
        ]

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации'
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=100
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение'
    )
    text = models.TextField('Описание блюда')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
        db_index=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[validator_coocing_time]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering=['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
            fields=['author', 'name'],
            name='unique_author_name'
            )
        ]

    def __str__(self):
        return self.name

class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipes',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[validator_amount]
    )
    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_ingredient_for_recipe'
            )
        ]

    def __str__(self) -> str:
        return (f'{self.recipe}: {self.ingredient},'
                f'{self.amount}, {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепты'
    )
    class Meta:
        verbose_name = 'Избраное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorited'
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe} в избранном : {self.user}'
        

class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепты'
    )
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipes_in_shopping_list'
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe} в списке покупок : {self.user}'

