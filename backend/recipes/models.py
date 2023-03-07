from django.db import models
from recipes.validators import validator_coocing_time, validator_amount

from users.models import User



class Tag(models.Model):
    """Модель Тэга для рецептов."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
        db_index=True
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
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name



class Ingredient(models.Model):
    """Модель ингредиентов рецепта."""
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
        db_index=True,
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
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации',
        db_index=True,
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=100
    )
    image = models.ImageField(
        upload_to='backend/media',
        verbose_name='Изображение'
    )
    text = models.TextField('Описание блюда')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
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

class IngredientRecipe(models.Model):
    """Модель связывания рецептов и ингредиентов с добавлением поля "amount" """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
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
    """Модель для избранных рецептов пользователей."""
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
        

class ShoppingCart(models.Model):
    """Модель списка покупок пользователей."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
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
