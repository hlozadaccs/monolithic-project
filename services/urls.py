from django.urls import path

from rest_framework import routers

from services import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'kitchen-logs', views.KitchenLogViewSet)
router.register(r'delivery-logs', views.DeliveryLogViewSet)


urlpatterns = [
    path('auth-login/', views.LoginView.as_view(), name='login'),
] + router.urls
