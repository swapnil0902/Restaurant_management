from django.urls import path
from .views import menu_view, create_menu_item_view, menu_item_detail_view

urlpatterns = [
    path('create/', create_menu_item_view, name='create-menu-item'),
    path('', menu_view, name='menu-view'),
    path('<int:pk>/', menu_item_detail_view, name='menu-detail'),
]
