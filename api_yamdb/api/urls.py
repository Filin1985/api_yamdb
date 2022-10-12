from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView


from .views import CategoryViewSet, GenreViewSet, TitleViewSet, AuthViewSet

app_name = 'api'

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'auth', AuthViewSet, basename='signup')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]