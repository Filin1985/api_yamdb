from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .serializers import SignUpSerializer, TokenSerializer

class AuthViewSet(ViewSet):
    """Вьюсет для отправки токена при регистрации."""
    @action(detail=True, methods=['post'])
    def signup(self, request, pk=None, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def token(self, request, pk=None, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.save()
            return Response({'token': token})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
