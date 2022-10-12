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

    def save(self, data):
        # password = str(randint(11111, 99999))
        password = '12345'
        user = User.objects.create(username=data['username'], email=data['email'])
        user.set_password(password)
        user.save()
        # send_confirmation_code(user.email, password)
        return user

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


class TitleSerializer(serializers.ModelSerializer):
    #category = serializers.DictField(required=False)
    # category = CategorySerializer(read_only=True, many=True)

    #category = serializers.SlugRelatedField(
    #    queryset=Category.objects.all(),
    #    required=False,
    #   slug_field='slug'
    #)
    # category = serializers.StringRelatedField(read_only=True)
    # category = serializers.SlugRelatedField(
    #    queryset=Category.objects.all(),
    #    required=False,
    #    slug_field='slug'
    #)
    # category_name = serializers.RelatedField(source='titles', read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre',
            'category'
        )
