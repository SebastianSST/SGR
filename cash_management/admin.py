from django.contrib import admin
from .models import CashRegister, PaymentMethod, Sale, DailyReport

@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ('register_number', 'opening_user', 'opening_time', 'closing_user', 'closing_time', 'status', 'total_sales')
    list_filter = ('status', 'opening_time', 'closing_time')
    search_fields = ('register_number', 'opening_user__username', 'closing_user__username')
    ordering = ('-opening_time',)
    readonly_fields = ('register_number', 'total_sales', 'total_cash', 'total_card', 'total_transfer')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'cash_register', 'created_at')
    list_filter = ('payment_method', 'created_at', 'cash_register')
    search_fields = ('order__order_number', 'cash_register__register_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_orders', 'total_sales', 'total_reservations', 'total_completed_reservations')
    list_filter = ('date',)
    search_fields = ('date',)
    ordering = ('-date',)
    readonly_fields = ('created_at', 'updated_at')
