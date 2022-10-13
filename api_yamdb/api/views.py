from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status, filters, mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    # TitleSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    SignUpSerializer,
    TokenSerializer
)

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment


class AuthViewSet(ViewSet):
    """Вьюсет для отправки токена при регистрации."""
    @action(detail=False, methods=['post'])
    def signup(self, request, pk=None, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def token(self, request, pk=None, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.save()
            return Response({'token': token})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleGetSerializer
    pagination_class = PageNumberPagination
    # разрешения прописать: POST -Администратор. GET - без токена !!!!
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleGetSerializer
        return TitlePostSerializer
