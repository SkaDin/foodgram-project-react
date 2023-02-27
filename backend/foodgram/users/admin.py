from django.contrib import admin

from users.models import User, Follow

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name')
    list_filter = ('email', 'first_name')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user', 'author')
