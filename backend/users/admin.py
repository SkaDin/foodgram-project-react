from django.contrib import admin
from users.models import User, Subscribers


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name'
    )
    list_filter = (
        'email',
        'first_name'
    )


@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    list_filter = (
        'user',
        'author'
    )
