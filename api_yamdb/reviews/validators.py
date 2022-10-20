from django.core.exceptions import ValidationError
from datetime import date


def validate_year(value):
    current_year = date.today().year
    if current_year < value:
        raise ValidationError(
            f'Год произведения {value} не может быть больше {current_year}'
        )
    return value
