from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from services import models
from services import serializer


User = get_user_model()


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = serializer.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not check_password(password, user.password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
        })


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer


class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializer.ProfileSerializer


class MenuItemViewSet(ModelViewSet):
    queryset = models.MenuItem.objects.all().order_by('category', 'name')
    serializer_class = serializer.MenuItemSerializer


class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all().select_related('user').prefetch_related('items__product')
    serializer_class = serializer.OrderSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = models.OrderItem.objects.select_related('order', 'product')
    serializer_class = serializer.OrderItemSerializer


class KitchenLogViewSet(ModelViewSet):
    queryset = models.KitchenLog.objects.select_related('order', 'order__user').all()
    serializer_class = serializer.KitchenLogSerializer


class DeliveryLogViewSet(ModelViewSet):
    queryset = models.DeliveryLog.objects.select_related('order', 'delivery_person').all()
    serializer_class = serializer.DeliveryLogSerializer
