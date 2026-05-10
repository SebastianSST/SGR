from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('subtotal',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'waiter', 'status', 'total_amount', 'table_number', 'created_at')
    list_filter = ('status', 'created_at', 'waiter')
    search_fields = ('order_number', 'customer__username', 'table_number')
    ordering = ('-created_at',)
    readonly_fields = ('order_number', 'total_amount')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Información de la Orden', {
            'fields': ('order_number', 'customer', 'waiter', 'status', 'table_number')
        }),
        ('Detalles Adicionales', {
            'fields': ('notes', 'total_amount')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'dish', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order__status', 'dish__category')
    search_fields = ('order__order_number', 'dish__name')
    readonly_fields = ('subtotal',)
