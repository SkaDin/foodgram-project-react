from django.urls import include, path

from rest_framework.routers import DefaultRouter
from api.views import (
    UsersSubscriptionsViewSet
)


router = DefaultRouter()

router.register(r'users', UsersSubscriptionsViewSet)
#router.register(r'recipes', )
#router.register(r'recipes', )
#router.register(r'recipes', )
#router.register(r'tags', )
#router.register(r'ingredients', )


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken'))
]
