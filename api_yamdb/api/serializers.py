import requests

from rest_framework import serializers

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment

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
