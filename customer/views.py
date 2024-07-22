from rest_framework import viewsets
from .models import Customer
from .serializer import CustomerSerializer
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import CustomerForm
from rest_framework.decorators import api_view, permission_classes

class CanEditCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.has_perm('customer.change_customer') and
            request.user.has_perm('customer.add_customer') and
            request.user.has_perm('customer.delete_customer')
        )

class CanViewCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('customer.view_customer')

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


@login_required
@csrf_protect
@permission_classes([IsAuthenticated, CanViewCustomer])
def customer_view(request):
    if request.user.groups.filter(name='Manager').exists():
        customers = Customer.objects.all()
        return render(request, 'customer/customer_list.html', {'customers': customers})
    else:
        customer = get_object_or_404(Customer, email=request.user.email)
        return redirect('customer-detail', pk=customer.pk)

@login_required
@csrf_protect
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_customer_view(request):
    if not request.user.groups.filter(name='Manager').exists():
        try:
            customer = Customer.objects.get(user=request.user)
            return redirect('customer-detail', pk=customer.pk)
        except Customer.DoesNotExist:
            if request.method == 'POST':
                form = CustomerForm(request.POST)
                if form.is_valid():
                    customer = form.save(commit=False)
                    customer.user = request.user
                    customer.email = request.user.email
                    customer.name = request.user.username
                    customer.save()
                    return redirect('customer-detail', pk=customer.pk)
            else:
                form = CustomerForm(initial={'name': request.user.username, 'email': request.user.email})
            return render(request, 'customer/customer_form.html', {'form': form})
    return redirect('customer-view')

@login_required
@csrf_protect
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated, CanEditCustomer])
def customer_detail_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if not request.user.groups.filter(name='Manager').exists() and customer.email != request.user.email:
        return redirect('customer-view')
    
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



