from django.contrib import admin
from .models import Reservation, Table

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_number', 'customer', 'date', 'time', 'number_of_guests', 'status', 'table_number')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('reservation_number', 'customer__username', 'table_number')
    ordering = ('-date', '-time')
    readonly_fields = ('reservation_number',)
    
    fieldsets = (
        ('Información de la Reserva', {
            'fields': ('reservation_number', 'customer', 'date', 'time', 'number_of_guests', 'table_number', 'status')
        }),
        ('Detalles Adicionales', {
            'fields': ('special_requests', 'contact_phone')
        }),
    )

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'status', 'location')
    list_filter = ('status', 'capacity')
    search_fields = ('number', 'location')
    ordering = ('number',)
