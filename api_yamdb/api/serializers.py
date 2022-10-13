from random import randint
import requests

from django.contrib.auth import authenticate
from django.conf import settings
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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


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
        read_only=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre',
            'category'
        )