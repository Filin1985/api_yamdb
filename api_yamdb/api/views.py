from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    # разрешения прописать: POST -Администратор. GET - без токена !!!!
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    # разрешения прописать: POST -Администратор. GET - без токена !!!!
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
