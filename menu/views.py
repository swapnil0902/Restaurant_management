from rest_framework import viewsets
from .models import menuItem
from .serializer import MenuSerializer
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import MenuItemForm
from rest_framework.decorators import api_view, permission_classes


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = menuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class CanEditMenu(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.has_perm('menu.change_menuitem') and
            request.user.has_perm('menu.add_menuitem') and
            request.user.has_perm('menu.delete_menuitem')
        )


class CanViewMenu(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('menu.view_menuitem')

@login_required
@csrf_protect
@permission_classes([IsAuthenticated])
def menu_view(request):
    menu_items = menuItem.objects.all()
    return render(request, 'menu/menu_items.html', {'menu_items': menu_items})

@login_required
@csrf_protect
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated, CanEditMenu])
def create_menu_item_view(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save':
                return redirect('menu-view')  
            elif action == 'save_and_add':
                context = {
                    'form': MenuItemForm(),
                    'alert': 'Menu item saved successfully!'
                }
                return render(request, 'menu/menu_item_form.html', context)
    else:
        form = MenuItemForm()
    return render(request, 'menu/menu_item_form.html', {'form': form})

@login_required
@csrf_protect
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated, CanEditMenu])
def menu_item_detail_view(request, pk):
    menu_item = get_object_or_404(menuItem, pk=pk)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('menu-item-detail', pk=pk)
    elif request.method == 'DELETE':
        menu_item.delete()
        return redirect('menu-view')
    
    form = MenuItemForm(instance=menu_item)
    return render(request, 'menu/menu_item_detail.html', {'menu_item': menu_item, 'form': form})