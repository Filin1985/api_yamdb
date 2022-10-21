
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from .validators import check_username

class User(AbstractUser):
    """Модель пользователя."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Админ'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = models.CharField(
        validators=[check_username],
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    confirmation_code = models.CharField(max_length=120, default='12345')
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='О себе'
    )
    role = models.CharField(
        max_length=max(len(value) for value, _ in ROLES),
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_staff
        )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    """Модель категории (типа) произведения (фильм, книга, музыка)."""
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='Ключ категории')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения. Одно произведение может быть привязано
     к нескольким жанрам."""
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, verbose_name='Ключ жанра')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения, к которым пишут отзывы."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(verbose_name='Год выпуска произведения')
    rating = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Рейтинг произведения'
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=256,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        through='GenreTitle',
        verbose_name='Жанр произведения',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    """Модель для связи id Title и id Genre."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзывов пользователей на произведения."""
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка произведения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Комментируемый отзыв",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор комментария",
    )
    text = models.TextField(verbose_name="Текст комментария")
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата комментария"
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:15]
