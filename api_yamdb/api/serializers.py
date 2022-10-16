import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment, User


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для запроса confirmation_code."""
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('username', 'email')    

    def validate_username(self, data):
        """Проверяем, что пользователь не использует имя 'me'."""
        if data.lower() == 'me':
            raise serializers.ValidationError("Данное имя пользователя использовать запрещено!")
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для запроса token."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
    

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        lookup_field = 'username'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre',
            'category'
        )


class TitlePostSerializer(serializers.ModelSerializer):
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
        if datetime.date.today().year < value:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
