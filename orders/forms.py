from django import forms
from .models import Order, OrderItem
from menu.models import Dish

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'notes']
        widgets = {
            'table_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity', 'notes']
        widgets = {
            'dish': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dish'].queryset = Dish.objects.filter(is_available=True)

OrderItemFormSet = forms.formset_factory(OrderItemForm, extra=1, min_num=1)
