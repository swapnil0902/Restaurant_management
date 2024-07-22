from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import menuItem, Restaurant
from .serializer import MenuSerializer, RestaurantSerializer
from .forms import MenuItemForm, RestaurantForm, RestaurantSelectForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test


User = get_user_model()

class CanEditMenu(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.has_perm('menu.change_menuitem') and
            request.user.has_perm('menu.add_menuitem') and
            request.user.has_perm('menu.delete_menuitem')
        )

class CanViewMenu(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('menu.view_menuitem')

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = menuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, CanEditMenu]

    # Specify the basename explicitly
    basename = 'menuitem'

    def get_queryset(self):
        user = self.request.user
        queryset = menuItem.objects.filter(restaurant__owner=user)
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, CanViewMenu])
    def my_menu(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def group_required(group_name):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if user.is_authenticated:
            return user.groups.filter(name=group_name).exists()
        return False
    return user_passes_test(in_groups)





@login_required
@csrf_protect
@permission_classes([permissions.IsAuthenticated, CanViewMenu])
def menu_view(request):
    user = request.user
    if user.groups.filter(name='Restaurant Owner').exists():
        try:
            restaurant = Restaurant.objects.get(owner=user)
            menu_items = menuItem.objects.filter(restaurant=restaurant)
            context = {
                'menu_items': menu_items,
                'restaurant_name': restaurant.name  # Pass the restaurant name to the template context
            }
            return render(request, 'menu/menu_items.html', context)
        except Restaurant.DoesNotExist:
            return redirect('create-restaurant')
    elif user.groups.filter(name='Manager').exists():
        restaurants = Restaurant.objects.all()
        return render(request, 'menu/restaurant_list.html', {'restaurants': restaurants})
    else:
        return redirect('view-or-write')  # or an appropriate error page
    
@login_required
@csrf_protect
@permission_classes([permissions.IsAuthenticated, CanViewMenu])    
def restaurant_menu_view(request, restaurant_id):
    user = request.user
    if user.groups.filter(name='Manager').exists():
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        menu_items = menuItem.objects.filter(restaurant=restaurant)
        context = {
                'menu_items': menu_items,
                'restaurant_name': restaurant.name  # Pass the restaurant name to the template context
            }
        return render(request, 'menu/menu_items.html', context)
    elif user.groups.filter(name='Restaurant Owner').exists():
        restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=user)
        menu_items = menuItem.objects.filter(restaurant=restaurant)
        context = {
                'menu_items': menu_items,
                'restaurant_name': restaurant.name  # Pass the restaurant name to the template context
            }
        return render(request, 'menu/menu_items.html', context)
    else:
        return redirect('view-or-write')  # or an appropriate error page

@login_required
@csrf_protect
@api_view(['POST', 'GET'])
@permission_classes([permissions.IsAuthenticated, CanEditMenu])

def create_menu_item_view(request):
    user = request.user
    
    if user.groups.filter(name='Manager').exists():
        if request.method == 'POST':
            select_form = RestaurantSelectForm(request.POST)
            if select_form.is_valid():
                selected_restaurant = select_form.cleaned_data['restaurant']
                form = MenuItemForm(request.POST)
                if form.is_valid():
                    menu_item = form.save(commit=False)
                    menu_item.restaurant = selected_restaurant
                    menu_item.save()
                    action = request.POST.get('action')
                    if action == 'save':
                        return redirect('menu-view')
                    elif action == 'save_and_add':
                        context = {
                            'form': MenuItemForm(),
                            'alert': 'Menu item saved successfully!',
                            'select_form': select_form
                        }
                        return render(request, 'menu/menu_item_form.html', context)
            else:
                form = MenuItemForm()
                select_form = RestaurantSelectForm()
        else:
            form = MenuItemForm()
            select_form = RestaurantSelectForm()
        
        return render(request, 'menu/menu_item_form.html', {'form': form, 'select_form': select_form})
    
    else:
        try:
            restaurant = Restaurant.objects.get(owner=user)
        except Restaurant.DoesNotExist:
            return redirect('create-restaurant')
        
        if request.method == 'POST':
            form = MenuItemForm(request.POST)
            if form.is_valid():
                menu_item = form.save(commit=False)
                menu_item.restaurant = restaurant
                menu_item.save()
                action = request.POST.get('action')
                if action == 'save':
                    return redirect('menu-view')
                elif action == 'save_and_add':
                    context = {
                        'form': MenuItemForm(),
                        'alert': 'Menu item saved successfully!',
                        'restaurant_name': restaurant.name
                    }
                    return render(request, 'menu/menu_item_form.html', context)
        else:
            form = MenuItemForm()
        
        return render(request, 'menu/menu_item_form.html', {'form': form, 'restaurant_name': restaurant.name})



@login_required
@csrf_protect
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated, CanEditMenu])
def menu_item_detail_view(request, pk):
    menu_item = get_object_or_404(menuItem, pk=pk, restaurant__owner=request.user)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('menu-item-detail', pk=pk)
    
    elif request.method == 'DELETE':
        menu_item.delete()
        return redirect('menu-view')
    
    elif request.method == 'GET':
        form = MenuItemForm(instance=menu_item)
        return render(request, 'menu/menu_item_detail.html', {'menu_item': menu_item, 'form': form})
    
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'DELETE'])








@login_required
@csrf_protect
@api_view(['POST', 'GET'])
@group_required('Restaurant Owner')
@permission_classes([permissions.IsAuthenticated])
def create_or_update_restaurant(request):
    user = request.user
    try:
        restaurant = Restaurant.objects.get(owner=user)
        form = RestaurantForm(request.POST or None, instance=restaurant)
    except Restaurant.DoesNotExist:
        restaurant = None
        form = RestaurantForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            if restaurant:
                form.save()
            else:
                new_restaurant = form.save(commit=False)
                new_restaurant.owner = user
                new_restaurant.save()
            return redirect('create-menu-item')

    context = {
        'form': form,
        'restaurant_name': restaurant.name if restaurant else None
    }
    return render(request, 'menu/create_or_update_restaurant.html', context)