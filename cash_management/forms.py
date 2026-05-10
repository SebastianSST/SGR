from django import forms
from django.utils import timezone
from .models import CashRegister, Sale

class CashRegisterOpenForm(forms.ModelForm):
    class Meta:
        model = CashRegister
        fields = ['opening_amount']
        widgets = {
            'opening_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

class CashRegisterCloseForm(forms.ModelForm):
    closing_amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'})
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    class Meta:
        model = CashRegister
        fields = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.status == 'open':
            self.fields['closing_amount'].initial = self.instance.opening_amount + self.instance.total_sales

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['payment_method', 'amount']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
