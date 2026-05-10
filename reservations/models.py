from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
        ('completed', 'Completada'),
    ]
    
    reservation_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    table_number = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"Reserva #{self.reservation_number} - {self.customer.username}"
    
    def save(self, *args, **kwargs):
        if not self.reservation_number:
            last_reservation = Reservation.objects.all().order_by('id').last()
            if last_reservation:
                res_num = int(last_reservation.reservation_number[3:]) + 1
            else:
                res_num = 1
            self.reservation_number = f"RES{res_num:06d}"
        super().save(*args, **kwargs)
    
    def clean(self):
        # Check if reservation date is in the past
        if self.date and self.date < timezone.now().date():
            raise ValidationError('No se pueden hacer reservas para fechas pasadas.')
        
        # Check if time is within business hours (example: 10 AM to 10 PM)
        if self.time:
            if self.time.hour < 10 or self.time.hour > 22:
                raise ValidationError('Las reservas solo se pueden hacer entre las 10:00 AM y las 10:00 PM.')

class Table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('occupied', 'Ocupada'),
        ('reserved', 'Reservada'),
        ('maintenance', 'En mantenimiento'),
    ]
    
    number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    location = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['number']
    
    def __str__(self):
        return f"Mesa {self.number} ({self.capacity} personas)"
