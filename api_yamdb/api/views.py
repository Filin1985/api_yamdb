from django.shortcuts import get_object_or_404

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.db.models import Avg
from rest_framework import status, filters, mixins, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from rest_framework.response import Response

from .permissions import (
    IsAdminOnly,
    IsAdminOrReadOnly,
    AdminOrModeratorOrAuthoOrIsReadOnly,
    AdminOrUnauthorizedOrAuthenticated
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    ReviewSerializer,
    CommentSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
)
from .utils import send_confirmation_code

from reviews.models import (
    Category, Genre, Title, GenreTitle, Review, Comment, User
)
from .filters import TitlesFilter


class AuthViewSet(ViewSet):
    """Вьюсет для отправки токена при регистрации."""
    @action(detail=False, methods=['post'],  permission_classes=[AllowAny])
    def signup(self, request, pk=None, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
            )
            if not created:
                confirmation_code = default_token_generator.make_token(user)
                User.objects.filter(username=username).update(
                    password=confirmation_code, is_active=True
                )
                send_confirmation_code(confirmation_code, email)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                confirmation_code = default_token_generator.make_token(user)
                User.objects.filter(username=username).update(
                    password=confirmation_code
                )
                confirmation_code = default_token_generator.make_token(user)
                User.objects.filter(username=username).update(
                    password=confirmation_code
                )
                send_confirmation_code(confirmation_code, email)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def token(self, request, pk=None, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data.get('confirmation_code')
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            if not default_token_generator.check_token(user, confirmation_code):
                return Response(
                    data={'error': 'Невалидный токен'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                data={'access': str(refresh.access_token)}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра и изменения данных пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                if serializer.validated_data.get('role'):
                    serializer.validated_data['role'] = request.user.role
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        AdminOrModeratorOrAuthoOrIsReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]

    def title_pk(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_pk())

    def get_queryset(self):
        return self.title_pk().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        AdminOrModeratorOrAuthoOrIsReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]

    def title_pk(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def review_pk(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'), title=self.title_pk()
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_pk())

    def get_queryset(self):
        return self.review_pk().comments.all()
