from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from services import models
from services import serializers


User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class MenuItemViewSet(ModelViewSet):
    queryset = models.MenuItem.objects.all().order_by('category', 'name')
    serializer_class = serializers.MenuItemSerializer


class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all().select_related('user').prefetch_related('items__product')
    serializer_class = serializers.OrderSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = models.OrderItem.objects.select_related('order', 'product')
    serializer_class = serializers.OrderItemSerializer


class KitchenLogViewSet(ModelViewSet):
    queryset = models.KitchenLog.objects.select_related('order', 'order__user').all()
    serializer_class = serializers.KitchenLogSerializer


class DeliveryLogViewSet(ModelViewSet):
    queryset = models.DeliveryLog.objects.select_related('order', 'delivery_person').all()
    serializer_class = serializers.DeliveryLogSerializer
