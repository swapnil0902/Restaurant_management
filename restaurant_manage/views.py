from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from customer.models import Customer

def home(request):
    return render(request, "restaurant_manage/index.html")

def view_or_write(request):
    return render(request, "restaurant_manage/view_or_write.html")

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def read_redirect(request):
    user = request.user
    if user.groups.filter(name='Restaurant Owner').exists():
        return redirect('menu-view')
    elif user.groups.filter(name='Customer').exists():
        customer = Customer.objects.filter(email=user.email).first()
        if customer:
            return redirect('customer-detail', pk=customer.pk)
    elif user.groups.filter(name='Manager').exists():
        return redirect('order-view')  # Make sure this URL name corresponds to the list of orders view
    return redirect('menu-view')

@login_required
def write_redirect(request):
    user = request.user
    if user.groups.filter(name='Restaurant Owner').exists():
        return redirect('create-menu-item')
    elif user.groups.filter(name='Customer').exists():
        customer = Customer.objects.filter(email=user.email).first()
        if customer:
            return redirect('create-order')
    elif user.groups.filter(name='Manager').exists():
        return redirect('create-menu-item')  # Make sure this URL name corresponds to the list of orders view
    return redirect('create-menu-item')