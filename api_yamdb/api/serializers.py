import datetime

from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment, User


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для запроса confirmation_code."""
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        fields = ('username', 'email')

    def validate_username(self, data):
        """Проверяем, что пользователь не использует имя 'me' и уникальность username."""
        if data.lower() == 'me':
            raise serializers.ValidationError(
                "Данное имя пользователя использовать запрещено!"
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для запроса token."""
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    confirmation_code = serializers.CharField(max_length=150)

    def validate_username(self, data):
        """Проверяем, что пользователь не использует имя 'me'."""
        if data.lower() == 'me':
            raise serializers.ValidationError(
                "Данное имя пользователя использовать запрещено!"
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    email = serializers.CharField(max_length=254)
    role = serializers.ChoiceField(
        choices=User.ROLES,
        default=User.USER,
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        lookup_field = 'username'

    def validate_username(self, data):
        """Проверяем, что пользователь не использует имя 'me'."""
        if data.lower() == 'me':
            raise serializers.ValidationError(
                "Данное имя пользователя использовать запрещено!"
            )
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError(
                "Пользователь с таким именем уже есть!"
            )
        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("Пользователь с такими email уже есть!")
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при GET запросах."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(source='reviews__score__avg')

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при POST, PATCH, PUT, FELETE запросах."""
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre',
            'category'
        )

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if datetime.date.today().year < value:
            raise serializers.ValidationError(
                f'Год выпуска {value} не может быть больше {current_year}'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title = get_object_or_404(
                Title,
                pk=self.context['view'].kwargs.get('title_id')
            )
            if Review.objects.filter(
                title=title,
                author=self.context['request'].user
            ).exists():
                raise ValidationError(
                    'Вы уже оставляли отзыв на данное произведение!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
