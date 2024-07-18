from rest_framework import viewsets
from .models import Customer
from .serializer import CustomerSerializer
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import CustomerForm
from rest_framework.decorators import api_view, permission_classes

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class CanEditCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.has_perm('customer.change_customer') and
            request.user.has_perm('customer.add_customer') and
            request.user.has_perm('customer.delete_customer')
        )


class CanViewCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('customer.view_menuitem')

@login_required
@csrf_protect
@permission_classes([IsAuthenticated, CanViewCustomer])
def customer_view(request):
    customers = Customer.objects.all()
    return render(request, 'customer/customer_list.html', {'customers': customers})

@login_required
@csrf_protect
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated, CanEditCustomer])
def create_customer_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save':
                return redirect('customer-view')  
            elif action == 'save_and_add':
                context = {
                    'form': CustomerForm(),
                    'alert': 'Customer saved successfully!'
                }
                return render(request, 'customer/customer_form.html', context)
    else:
        form = CustomerForm()
    return render(request, 'customer/customer_form.html', {'form': form})

@login_required
@csrf_protect
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated, CanEditCustomer])
def customer_detail_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer-detail', pk=pk)
    elif request.method == 'DELETE':
        customer.delete()
        return redirect('customer-view')
    
    form = CustomerForm(instance=customer)
    return render(request, 'customer/customer_detail.html', {'customer': customer, 'form': form})