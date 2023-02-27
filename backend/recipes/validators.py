from django.core.exceptions import ValidationError


def validator_coocing_time(value):
    if value < 1:
        raise ValidationError('Время приготовления должно быть больше минуты!')


def validator_amount(value):
    if value < 0.01:
        raise ValidationError('Количество должно быть больше нуля!')
