from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError



class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        max_length=150
    )
    last_name = models.CharField(
        max_length=150
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user'
            )
        ]

    def __str__(self):
        return self.username


class Subscribers(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'user'),
                name='unique_follower'
            )
        ]

    def save(self, **kwargs):
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя!')
        super().save()
