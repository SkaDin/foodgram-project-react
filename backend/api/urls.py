from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ( 
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    UsersViewSet
)

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.authtoken')),
]
