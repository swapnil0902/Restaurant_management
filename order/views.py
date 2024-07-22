from rest_framework import viewsets
from customer.models import Customer
from menu.models import menuItem, Restaurant
from .models import Order
from .serializer import OrderSerializer
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import OrderForm, RestaurantSelectionForm, OrderEditForm
from rest_framework.decorators import api_view, permission_classes
import csv
from django.http import HttpResponse


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class CanEditOrder(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.has_perm('order.change_order') and
            request.user.has_perm('order.add_order') and
            request.user.has_perm('order.delete_order')
        )


class CanViewOrder(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('order.view_order')

@login_required
@csrf_protect
@permission_classes([IsAuthenticated, CanViewOrder])
def order_view(request):
    user = request.user
    
    if user.groups.filter(name='Manager').exists():
        orders = Order.objects.all()
    elif user.groups.filter(name='Restaurant Owner').exists():
        try:
            restaurant = get_object_or_404(Restaurant, owner=user)
            orders = Order.objects.filter(menu_item__restaurant=restaurant)
        except Restaurant.DoesNotExist:
            orders = Order.objects.none()
    else:  # Customer
        try:
            customer = Customer.objects.get(user=user)
            orders = Order.objects.filter(customer=customer)
        except Customer.DoesNotExist:
            orders = Order.objects.none()
        
    return render(request, 'order/order_history.html', {'orders': orders})

@login_required
@csrf_protect
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated, CanEditOrder])
def create_order_view(request, restaurant_id=None):
    if request.user.groups.filter(name='Manager').exists():
        orders = Order.objects.all()
        return render(request, 'order/order_history.html', {'orders': orders})
    else:
        customer = get_object_or_404(Customer, user=request.user)
        
        if request.method == 'POST':
            if restaurant_id is None:
                form = RestaurantSelectionForm(request.POST)
                if form.is_valid():
                    restaurant_id = form.cleaned_data['restaurant'].id
                    return redirect('create-order-restaurant', restaurant_id=restaurant_id)
            else:
                restaurant = get_object_or_404(Restaurant, id=restaurant_id)
                form = OrderForm(request.POST, restaurant=restaurant)
                if form.is_valid():
                    menu_items = form.cleaned_data['menu_items']
                    quantities = form.cleaned_data['quantities'].split(',')
                    
                    for menu_item, quantity in zip(menu_items, quantities):
                        order = Order(
                            menu_item=menu_item,
                            customer=customer,
                            menu_name=menu_item.name,
                            customer_name=customer.name,
                            quantity=int(quantity.strip()),
                            rate=menu_item.price,
                            total_price=int(quantity.strip()) * menu_item.price
                        )
                        order.save()
                    
                    action = request.POST.get('action')
                    if action == 'save':
                        return redirect('order-view')
                    elif action == 'save_and_add':
                        context = {
                            'form': OrderForm(restaurant=restaurant),
                            'alert': 'Orders saved successfully!',
                            'restaurant': restaurant
                        }
                        return render(request, 'order/order_form.html', context)
        else:
            if restaurant_id is not None:
                restaurant = get_object_or_404(Restaurant, id=restaurant_id)
                form = OrderForm(restaurant=restaurant)
                return render(request, 'order/order_form.html', {'form': form, 'restaurant': restaurant})
            else:
                form = RestaurantSelectionForm()
        return render(request, 'order/select_restaurant.html', {'form': form})


@login_required
@csrf_protect
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated, CanEditOrder])
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    restaurant = order.menu_item.restaurant  # Get the restaurant of the original order
    
    # Filter menu items by the restaurant
    menu_items = menuItem.objects.filter(restaurant=restaurant)

    if request.method == 'POST':
        if 'delete' in request.POST:
            order.delete()
            return redirect('order-view')
        else:
            form = OrderEditForm(request.POST, instance=order, restaurant=restaurant)
            if form.is_valid():
                # Save the form data and update the total price
                order = form.save(commit=False)
                order.rate = order.menu_item.price
                order.total_price = order.quantity * order.rate
                order.save()
                return redirect('order-detail', pk=pk)
    else:
        form = OrderEditForm(instance=order, restaurant=restaurant)
    
    return render(request, 'order/order_detail.html', {
        'order': order,
        'form': form,
        'menu_items': menu_items
    })

def print_order_history(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer Name', 'Order Date', 'Total Amount'])

    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.customer_id, order.order_date, order.total_price])

    return response 



def handler403(request, exception=None):
    return render(request, 'restaurant_manage/403.html', status=403)

