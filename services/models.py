from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserRole(models.TextChoices):
    CUSTOMER = "CUSTOMER", "Cliente"
    WAITER = "WAITER", "Mesero"
    CHEF = "CHEF", "Cocinero"
    DELIVERY = "DELIVERY", "Repartidor"
    CASHIER = "CASHIER", "Cajero"


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        null=True,
        blank=True,
        default=None
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email})"

    def __repr__(self):
        return f"<User: {self.email}>"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    address = models.TextField(
        null=True,
        blank=True,
    )
    lat = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )
    lng = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
    )

    def __str__(self):
        return f"{self.user.email})"

    def __repr__(self):
        return f"<Profile: {self.user.email}>"
    
    def clean(self):
        super().clean()
        if (self.lat is None) != (self.lng is None):
            raise ValidationError(
                "Both latitude and longitude must be set together"
                " or left empty."
            )


class MenuCategory(models.TextChoices):
    APPETIZER = "APPETIZER", "Entrada"
    MAIN_COURSE = "MAIN_COURSE", "Plato Principal"
    DESSERT = "DESSERT", "Postre"
    SOFT_DRINK = "SOFT_DRINK", "Gaseosa"
    JUICE = "JUICE", "Jugo"
    ALCOHOLIC_BEVERAGE = "ALCOHOL", "Bebida Alcohólica"
    OTHER = "OTHER", "Otro"


class MenuItem(models.Model):
    name = models.CharField(
        max_length=100
    )
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=MenuCategory.choices,
        default=MenuCategory.OTHER,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<MenuItem: {self.name}>"
    
    @property
    def category_label(self):
        return self.get_category_display()


class OrderStatus(models.TextChoices):
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


class OrderType(models.TextChoices):
    DINE_IN = "DINE_IN", "Para comer aquí"
    TAKEAWAY = "TAKEAWAY", "Para llevar"
    DELIVERY = "DELIVERY", "Entrega a domicilio"


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    order_type = models.CharField(
        max_length=20,
        choices=OrderType.choices,
        default=OrderType.DINE_IN
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user.first_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    notes = models.TextField(
        blank=True,
        null=True
    )


class KitchenAction(models.TextChoices):
    RECEIVED = "RECEIVED", "Recibido"
    STARTED = "STARTED", "En preparación"
    READY = "READY", "Listo"
    CANCELED = "CANCELED", "Cancelado"


class KitchenLog(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='kitchen_logs'
    )
    action = models.CharField(
        max_length=20,
        choices=KitchenAction.choices
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Order #{self.order.id} - {self.get_action_display()} @ {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class DeliveryStatus(models.TextChoices):
    ASSIGNED = "ASSIGNED", "Repartidor asignado"
    DISPATCHED = "DISPATCHED", "Despachado"
    ON_THE_WAY = "ON_THE_WAY", "En camino"
    DELIVERED = "DELIVERED", "Entregado"
    FAILED = "FAILED", "Fallido"
    CANCELED = "CANCELED", "Cancelado"


class DeliveryLog(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery_logs'
    )
    delivery_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'DELIVERY'}
    )
    status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Order #{self.order.id} - {self.get_status_display()} @ {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class InvoiceStatus(models.TextChoices):
    GENERATED = "GENERATED", "Generada"
    PAID = "PAID", "Pagada"
    CANCELED = "CANCELED", "Cancelada"


class Invoice(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='invoice'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.GENERATED
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Factura #{self.id} para orden #{self.order.id}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_name = models.CharField(
        max_length=100
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
