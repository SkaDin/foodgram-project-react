from django.contrib import admin

from recipes.models import (
    Recipe,
    Ingredient,
    Tag,
    IngredientRecipe,
    Favorite,
    ShoppingCart
)

class RecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author'
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    inlines = [
        RecipeInline,
    ]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color'
    )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    

@admin.register(ShoppingCart)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user'
    )


@admin.register(IngredientRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )

