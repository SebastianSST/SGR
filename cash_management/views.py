from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
import datetime
from .models import CashRegister, Sale, DailyReport
from .forms import CashRegisterOpenForm, CashRegisterCloseForm
from orders.models import Order
from reservations.models import Reservation

@login_required
def dashboard(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para acceder al dashboard de caja.')
        return redirect('dashboard')
    
    today = timezone.now().date()
    
    # Get today's stats
    today_orders = Order.objects.filter(created_at__date=today, status='delivered').count()
    today_sales = Sale.objects.filter(created_at__date=today).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    today_reservations = Reservation.objects.filter(date=today).count()
    completed_reservations = Reservation.objects.filter(date=today, status='completed').count()
    
    # Get current open register
    open_register = CashRegister.objects.filter(status='open').first()
    
    # Get recent sales
    recent_sales = Sale.objects.select_related('order').order_by('-created_at')[:10]
    
    context = {
        'today_orders': today_orders,
        'today_sales': today_sales,
        'today_reservations': today_reservations,
        'completed_reservations': completed_reservations,
        'open_register': open_register,
        'recent_sales': recent_sales,
    }
    return render(request, 'cash_management/dashboard.html', context)

@login_required
def open_register(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para abrir caja.')
        return redirect('dashboard')
    
    # Check if there's already an open register
    open_register = CashRegister.objects.filter(status='open').first()
    if open_register:
        messages.error(request, 'Ya hay una caja abierta.')
        return redirect('cash:dashboard')
    
    if request.method == 'POST':
        form = CashRegisterOpenForm(request.POST)
        if form.is_valid():
            register = form.save(commit=False)
            register.opening_user = request.user
            register.save()
            messages.success(request, 'Caja abierta exitosamente.')
            return redirect('cash:dashboard')
    else:
        form = CashRegisterOpenForm()
    
    return render(request, 'cash_management/open_register.html', {'form': form})

@login_required
def close_register(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para cerrar caja.')
        return redirect('dashboard')
    
    open_register = CashRegister.objects.filter(status='open').first()
    if not open_register:
        messages.error(request, 'No hay ninguna caja abierta.')
        return redirect('cash:dashboard')
    
    if request.method == 'POST':
        form = CashRegisterCloseForm(request.POST, instance=open_register)
        if form.is_valid():
            closing_amount = form.cleaned_data['closing_amount']
            notes = form.cleaned_data['notes']
            open_register.close(closing_amount, request.user, notes)
            messages.success(request, 'Caja cerrada exitosamente.')
            return redirect('cash:dashboard')
    else:
        form = CashRegisterCloseForm(instance=open_register)
    
    return render(request, 'cash_management/close_register.html', {
        'form': form,
        'register': open_register
    })

@login_required
def daily_report(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para ver reportes.')
        return redirect('dashboard')
    
    date_str = request.GET.get('date')
    if date_str:
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = timezone.now().date()
    else:
        date = timezone.now().date()
    
    # Get or create daily report
    report, created = DailyReport.objects.get_or_create(
        date=date,
        defaults={
            'total_orders': Order.objects.filter(created_at__date=date, status='delivered').count(),
            'total_reservations': Reservation.objects.filter(date=date).count(),
            'total_completed_reservations': Reservation.objects.filter(date=date, status='completed').count(),
        }
    )
    
    # Update sales data
    sales_data = Sale.objects.filter(created_at__date=date).aggregate(
        total=Sum('amount'),
        cash=Sum('amount', filter=Q(payment_method='cash')),
        card=Sum('amount', filter=Q(payment_method='card')),
        transfer=Sum('amount', filter=Q(payment_method='transfer'))
    )
    
    report.total_sales = sales_data['total'] or 0
    report.total_cash_sales = sales_data['cash'] or 0
    report.total_card_sales = sales_data['card'] or 0
    report.total_transfer_sales = sales_data['transfer'] or 0
    report.save()
    
    # Get detailed orders and sales
    orders = Order.objects.filter(created_at__date=date, status='delivered').order_by('-created_at')
    sales = Sale.objects.filter(created_at__date=date).select_related('order').order_by('-created_at')
    
    context = {
        'report': report,
        'orders': orders,
        'sales': sales,
        'selected_date': date,
    }
    return render(request, 'cash_management/daily_report.html', context)

@login_required
def register_history(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para ver el historial de cajas.')
        return redirect('dashboard')
    
    registers = CashRegister.objects.all().order_by('-opening_time')
    return render(request, 'cash_management/register_history.html', {'registers': registers})

@login_required
def export_daily_report(request):
    if request.user.user_type not in ['waiter', 'admin']:
        messages.error(request, 'No tienes permisos para exportar reportes.')
        return redirect('dashboard')
    
    date_str = request.GET.get('date')
    if date_str:
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = timezone.now().date()
    else:
        date = timezone.now().date()
    
    report = DailyReport.objects.filter(date=date).first()
    if not report:
        messages.error(request, 'No hay reporte disponible para esta fecha.')
        return redirect('cash:daily_report')
    
    # Generate CSV report
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reporte_diario_{date}.csv"'
    
    csv_content = render_to_string('cash_management/daily_report.csv', {'report': report})
    response.write(csv_content)
    
    return response
