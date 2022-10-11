from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
app_name = 'api'
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('v1/jwt/', include('djoser.urls')), # управление пользователями
    # path('v1/', include('djoser.urls.jwt')),
]