from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    """Модель категории (типа) произведения (фильм, книга, музыка)."""
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='Ключ категории')

    class Meta:
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
    # rating, вероятно, расчетное и в самой модели избыточно, а мт и нет???
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
        # null=True,
        blank=True,
        # on_delete=models.SET_NULL, # миграции не проходили
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
        ordering = ('year',)
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
    # должна быть валидация score от 1 до 10
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

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    pass
