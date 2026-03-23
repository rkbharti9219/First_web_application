from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'product',
        'product_name',
        'price',
        'quantity',
        'total_price',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'status',
        'payment_method',
        'total_amount',
        'created_at',
    )
    list_filter = (
        'status',
        'payment_method',
        'payment_status',
    )
    list_editable = ('status',)
    search_fields = (
        'user__username',
        'full_name',
        'email',
        'phone',
    )
    inlines = [OrderItemInline]