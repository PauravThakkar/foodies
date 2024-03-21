from django.shortcuts import render, redirect
from .models import Restaurant, MenuItem, Admin
from .forms import MenuItemForm


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})


def menu_items(request, restaurant_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'menu_items.html', {'restaurant': restaurant, 'menu_items': menu_items})


def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html', {'form': form})
