from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Category, Dish
from .forms import CategoryForm, DishForm

def menu_list(request):
    categories = Category.objects.filter(is_active=True)
    dishes = Dish.objects.filter(is_available=True)
    
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    if category_id:
        dishes = dishes.filter(category_id=category_id)
    
    if search_query:
        dishes = dishes.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'categories': categories,
        'dishes': dishes,
        'selected_category': category_id,
        'search_query': search_query,
    }
    return render(request, 'menu/menu_list.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'menu/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('menu:category_list')
    else:
        form = CategoryForm()
    return render(request, 'menu/category_form.html', {'form': form, 'title': 'Crear Categoría'})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('menu:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'menu/category_form.html', {'form': form, 'title': 'Editar Categoría'})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('menu:category_list')
    return render(request, 'menu/category_confirm_delete.html', {'category': category})

def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'menu/dish_list.html', {'dishes': dishes})

def dish_create(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato creado exitosamente.')
            return redirect('menu:dish_list')
    else:
        form = DishForm()
    return render(request, 'menu/dish_form.html', {'form': form, 'title': 'Crear Plato'})

def dish_edit(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato actualizado exitosamente.')
            return redirect('menu:dish_list')
    else:
        form = DishForm(instance=dish)
    return render(request, 'menu/dish_form.html', {'form': form, 'title': 'Editar Plato'})

def dish_delete(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        dish.delete()
        messages.success(request, 'Plato eliminado exitosamente.')
        return redirect('menu:dish_list')
    return render(request, 'menu/dish_confirm_delete.html', {'dish': dish})
