from django import forms
from django.utils import timezone
from .models import Reservation, Table

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_guests', 'table_number', 'special_requests', 'contact_phone']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': timezone.now().date()}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '20'}),
            'table_number': forms.TextInput(attrs={'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']
        self.fields['time'].input_formats = ['%H:%M']

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'capacity', 'status', 'location']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '20'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
