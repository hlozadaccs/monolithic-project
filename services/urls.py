from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from services import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"profiles", views.ProfileViewSet)
router.register(r"orders", views.OrderViewSet)
router.register(r"order-items", views.OrderItemViewSet)
router.register(r"kitchen-logs", views.KitchenLogViewSet)
router.register(r"delivery-logs", views.DeliveryLogViewSet)


urlpatterns = (
    [
        path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    ]
    + router.urls
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
