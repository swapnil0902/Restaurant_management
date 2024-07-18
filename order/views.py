from rest_framework import viewsets
from .models import Order
from .serializer import OrderSerializer
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import OrderForm
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
    orders = Order.objects.all()
    return render(request, 'order/order_history.html', {'orders': orders})

@login_required
@csrf_protect
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated, CanEditOrder])
def create_order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save':
                return redirect('order-view')  
            elif action == 'save_and_add':
                context = {
                    'form': OrderForm(),
                    'alert': 'Order saved successfully!'
                }
                return render(request, 'order/order_form.html', context)
    else:
        form = OrderForm()
    return render(request, 'order/order_form.html', {'form': form})

@login_required
@csrf_protect
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated, CanEditOrder])
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order-detail', pk=pk)
    elif request.method == 'DELETE':
        order.delete()
        return redirect('order-view')
    
    form = OrderForm(instance=order)
    return render(request, 'order/order_detail.html', {'order': order, 'form': form})

def print_order_history(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer Name', 'Order Date', 'Total Amount'])

    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.customer_id, order.order_date, order.total_price])

    return response 