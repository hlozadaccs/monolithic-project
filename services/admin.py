from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from services import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Role Info'), {'fields': ('role',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'address', 'lat', 'lng', 'has_coordinates')
    search_fields = ('user__email', 'address')
    list_filter = ('lat', 'lng')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def has_coordinates(self, obj):
        return obj.lat is not None and obj.lng is not None

    has_coordinates.boolean = True
    has_coordinates.short_description = 'Has Coordinates'


@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_label', 'price', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    list_editable = ('available',)

    def category_label(self, obj):
        return obj.get_category_display()

    category_label.short_description = 'Categoría'


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'status')
    list_filter = ('order_type', 'status', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)
    inlines = [OrderItemInline]


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__user__email', 'product__name')


@admin.register(models.KitchenLog)
class KitchenLogAdmin(admin.ModelAdmin):
    list_display = ('order', 'action', 'created_at', 'updated_at')
    list_filter = ('action', 'created_at')
    search_fields = ('order__id', 'order__user__email', 'action')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(models.DeliveryLog)
class DeliveryLogAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'delivery_user', 'created_at', 'updated_at')
    list_filter = ('status', 'delivery_user', 'created_at')
    search_fields = ('order__id', 'delivery_user__email', 'status')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
