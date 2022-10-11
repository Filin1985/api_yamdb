from rest_framework import serializers

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
