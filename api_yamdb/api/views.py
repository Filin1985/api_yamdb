from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models import Avg
from rest_framework import status, filters, mixins, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from .permissions import IsAdminOnly, IsAdminOrModeratorOnly, IsReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    ReviewSerializer,
    CommentSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer
)

from reviews.models import (
    Category, Genre, Title, GenreTitle, Review, Comment, User
)


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

class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра и изменения данных пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOnly,)
    pagination_class = PageNumberPagination


class ProfileViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра и изменения данных пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated, )
    
    @action(detail=True, methods=['get'], url_path='v1/users/me')
    def get_user(self, request, pk=None):
        user = self.get_object()
        print(user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    search_fields = ('slug',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    search_fields = ('slug',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = PageNumberPagination
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')
    # разрешения прописать: POST -Администратор. GET - без токена !!!!
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def title_pk(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_pk())

    def get_queryset(self):
        #return Review.objects.filter(title=self.kwargs.get('title_id'))
        return self.title_pk().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def title_pk(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def review_pk(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'), title=self.title_pk()
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_pk())

    def get_queryset(self):
        #return Comment.objects.filter(review=self.kwargs.get('review_id'))
        return self.review_pk().comments.all()
