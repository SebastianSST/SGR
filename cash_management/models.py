from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

class CashRegister(models.Model):
    STATUS_CHOICES = [
        ('open', 'Abierta'),
        ('closed', 'Cerrada'),
    ]
    
    register_number = models.CharField(max_length=20, unique=True)
    opening_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opened_registers')
    closing_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='closed_registers')
    opening_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    closing_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_card = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_transfer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    opening_time = models.DateTimeField(auto_now_add=True)
    closing_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-opening_time']
    
    def __str__(self):
        return f"Caja #{self.register_number} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        if not self.register_number:
            last_register = CashRegister.objects.all().order_by('id').last()
            if last_register:
                reg_num = int(last_register.register_number[3:]) + 1
            else:
                reg_num = 1
            self.register_number = f"CASH{reg_num:06d}"
        super().save(*args, **kwargs)
    
    def close(self, closing_amount, closing_user, notes=''):
        self.closing_amount = closing_amount
        self.closing_user = closing_user
        self.closing_time = timezone.now()
        self.status = 'closed'
        self.notes = notes
        self.save()

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
    ]
    
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, related_name='sales')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Venta #{self.id} - ${self.amount}"

class DailyReport(models.Model):
    date = models.DateField(unique=True)
    total_orders = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cash_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_card_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_transfer_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_reservations = models.PositiveIntegerField(default=0)
    total_completed_reservations = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Reporte del {self.date}"
