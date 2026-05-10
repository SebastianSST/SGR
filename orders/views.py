from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet
from menu.models import Dish

@login_required
def order_list(request):
    user = request.user
    if user.user_type == 'client':
        orders = Order.objects.filter(customer=user)
    elif user.user_type == 'waiter':
        orders = Order.objects.filter(Q(waiter=user) | Q(waiter__isnull=True))
    else:  # admin
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

@login_required
def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.customer = request.user
            if request.user.user_type == 'waiter':
                order.waiter = request.user
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

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    # Check permissions
    if (request.user.user_type == 'client' and order.customer != request.user) or \
       (request.user.user_type == 'waiter' and order.waiter != request.user and order.waiter is not None):
        messages.error(request, 'No tienes permisos para ver esta orden.')
        return redirect('orders:order_list')
    
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
@require_POST
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        if request.user.user_type == 'waiter' and not order.waiter:
            order.waiter = request.user
        order.save()
        return JsonResponse({'success': True, 'status': order.get_status_display()})
    
    return JsonResponse({'success': False}, status=400)

@login_required
def kitchen_orders(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')
    
    orders = Order.objects.filter(status__in=['confirmed', 'preparing']).order_by('created_at')
    return render(request, 'orders/kitchen_orders.html', {'orders': orders})

@login_required
def take_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.user.user_type != 'waiter':
        messages.error(request, 'Solo los meseros pueden tomar órdenes.')
        return redirect('orders:order_list')
    
    if order.waiter is None:
        order.waiter = request.user
        order.status = 'confirmed'
        order.save()
        messages.success(request, 'Orden tomada exitosamente.')
    else:
        messages.info(request, 'Esta orden ya ha sido tomada.')
    
    return redirect('orders:order_detail', pk=order.pk)
