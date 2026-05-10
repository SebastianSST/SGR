from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Reservation, Table
from .forms import ReservationForm, TableForm

@login_required
def reservation_list(request):
    user = request.user
    if user.user_type == 'client':
        reservations = Reservation.objects.filter(customer=user)
    else:  # waiter or admin
        reservations = Reservation.objects.all()
    
    status_filter = request.GET.get('status')
    date_filter = request.GET.get('date')
    
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    
    if date_filter:
        reservations = reservations.filter(date=date_filter)
    
    context = {
        'reservations': reservations,
        'status_choices': Reservation.STATUS_CHOICES,
        'current_status': status_filter,
        'current_date': date_filter,
    }
    return render(request, 'reservations/reservation_list.html', context)

@login_required
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user
            reservation.save()
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('reservations:reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm()
    
    return render(request, 'reservations/reservation_form.html', {
        'form': form,
        'title': 'Crear Reserva'
    })

@login_required
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Check permissions
    if request.user.user_type == 'client' and reservation.customer != request.user:
        messages.error(request, 'No tienes permisos para ver esta reserva.')
        return redirect('reservations:reservation_list')
    
    return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})

@login_required
def reservation_edit(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Check permissions
    if request.user.user_type == 'client' and reservation.customer != request.user:
        messages.error(request, 'No tienes permisos para editar esta reserva.')
        return redirect('reservations:reservation_list')
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada exitosamente.')
            return redirect('reservations:reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm(instance=reservation)
    
    return render(request, 'reservations/reservation_form.html', {
        'form': form,
        'title': 'Editar Reserva'
    })

@login_required
def reservation_cancel(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Check permissions
    if request.user.user_type == 'client' and reservation.customer != request.user:
        messages.error(request, 'No tienes permisos para cancelar esta reserva.')
        return redirect('reservations:reservation_list')
    
    if reservation.status in ['confirmed', 'pending']:
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Reserva cancelada exitosamente.')
    else:
        messages.error(request, 'No se puede cancelar esta reserva.')
    
    return redirect('reservations:reservation_detail', pk=reservation.pk)

@login_required
def reservation_confirm(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para confirmar reservas.')
        return redirect('reservations:reservation_list')
    
    if reservation.status == 'pending':
        reservation.status = 'confirmed'
        reservation.save()
        messages.success(request, 'Reserva confirmada exitosamente.')
    else:
        messages.error(request, 'Esta reserva ya no puede ser confirmada.')
    
    return redirect('reservations:reservation_detail', pk=reservation.pk)

@login_required
def table_list(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para ver las mesas.')
        return redirect('dashboard')
    
    tables = Table.objects.all()
    return render(request, 'reservations/table_list.html', {'tables': tables})

@login_required
def table_create(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para crear mesas.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesa creada exitosamente.')
            return redirect('reservations:table_list')
    else:
        form = TableForm()
    
    return render(request, 'reservations/table_form.html', {
        'form': form,
        'title': 'Crear Mesa'
    })

@login_required
def calendar_view(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para ver el calendario.')
        return redirect('dashboard')
    
    # Get current month reservations
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    reservations = Reservation.objects.filter(
        date__gte=start_of_month,
        date__lte=end_of_month,
        status__in=['pending', 'confirmed']
    ).order_by('date', 'time')
    
    context = {
        'reservations': reservations,
        'current_date': today,
    }
    return render(request, 'reservations/calendar.html', context)
