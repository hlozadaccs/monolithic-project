from rest_framework import serializers

from services import models


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = models.MenuItem
        fields = ['id', 'name', 'description', 'category', 'category_label', 'price', 'available']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'product_name', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.ReadOnlyField(source='user.email')
    order_type_label = serializers.CharField(source='get_order_type_display', read_only=True)

    class Meta:
        model = models.Order
        fields = ['id', 'user', 'user_email', 'order_type', 'order_type_label', 'status', 'items', 'created_at', 'updated_at',]


class KitchenLogSerializer(serializers.ModelSerializer):
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = models.KitchenLog
        fields = ['id', 'order', 'action', 'action_display', 'notes', 'created_at', 'updated_at']


class DeliveryLogSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    delivery_person_email = serializers.ReadOnlyField(source='delivery_person.email')

    class Meta:
        model = models.DeliveryLog
        fields = ['id', 'order', 'delivery_person', 'delivery_person_email', 'status', 'status_display', 'notes', 'created_at', 'updated_at']
