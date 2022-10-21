from datetime import date
import re

from django.core.exceptions import ValidationError

REGEX_USERNAME = re.compile(r'^[\w.@+-]+\Z')

def validate_year(value):
    current_year = date.today().year
    if current_year < value:
        raise ValidationError(
            f'Год произведения {value} не может быть больше {current_year}'
        )
    return value

def check_username(value):
    """Проверяем, что пользователь не использует имя 'me'."""
    if value == 'me':
        raise ValidationError(
            f'Имя {value} пользователя использовать запрещено!'
        )
    if not REGEX_USERNAME.fullmatch(value):
        raise ValidationError(
            f'Используйте только цифры, буквы и символы ".@+-".'
        )
