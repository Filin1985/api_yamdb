from random import randint
import requests
import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from django.db.models import Avg
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from reviews.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def save(self):
        user = User.objects.create(username=self.validated_data['username'], email=self.validated_data['email'])
        confirmation_code = hash(user.email)
        user.set_password(confirmation_code)
        user.save()
        send_mail(
            'Confirmation Code',
            f'Your confirmation code: {str(confirmation_code)}',
            'django2022@gmail.com',
            [user.email, ],
            fail_silently=False
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def save(self):
        user = authenticate(username=self.validated_data['username'], password=self.validated_data['confirmation_code'])
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError("Данное имя пользователя использовать запрещено!")
        return data


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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre',
            'category'
        )

    def get_rating(self, obj):
        return Review.objects.filter(title=obj).aggregate(
            Avg('score'))['score__avg']


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
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Вы уже оставляли отзыв на данное произведение!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
