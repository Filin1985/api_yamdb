from random import randint
import requests

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from reviews.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def save(self):
        # password = str(randint(11111, 99999))
        password = '12345'
        user = User.objects.create(username=self.validated_data['username'], email=self.validated_data['email'])
        user.set_password(password)
        user.save()
        # send_confirmation_code(user.email, password)
        return user

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def save(self, data):
        user = authenticate(username=data['username'], password=data['confirmation_code'])
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


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