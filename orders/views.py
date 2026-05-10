from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet
from menu.models import Dish

def order_list(request):
    # Simplified for demo - show all orders
    orders = Order.objects.all()
    
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'orders/order_list.html', context)

def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            # Simplified for demo - no user assignment
            order.save()
            
            total_amount = 0
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    item = form.save(commit=False)
                    item.order = order
                    item.unit_price = item.dish.price
                    item.save()
                    total_amount += item.subtotal
            
            order.total_amount = total_amount
            order.save()
            
            messages.success(request, 'Orden creada exitosamente.')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()
    
    return render(request, 'orders/order_form.html', {
        'order_form': order_form,
        'formset': formset,
        'title': 'Crear Orden'
    })

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})

@require_POST
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        return JsonResponse({'success': True, 'status': order.get_status_display()})
    
    return JsonResponse({'success': False}, status=400)

def kitchen_orders(request):
    orders = Order.objects.filter(status__in=['confirmed', 'preparing']).order_by('created_at')
    return render(request, 'orders/kitchen_orders.html', {'orders': orders})

def take_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if order.waiter is None:
        order.status = 'confirmed'
        order.save()
        messages.success(request, 'Orden tomada exitosamente.')
    else:
        messages.info(request, 'Esta orden ya ha sido tomada.')
    
    return redirect('orders:order_detail', pk=order.pk)
