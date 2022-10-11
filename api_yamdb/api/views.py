from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import filters, mixins, permissions, viewsets

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from .serializers import (CategorySerializer, )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # разрешения прописать: POST -Администратор. GET - без токена !!!!
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)