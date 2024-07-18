from django.urls import path
from .views import order_view, create_order_view, order_detail_view, print_order_history

urlpatterns = [
    path('', order_view, name='order-view'),
    path('create/', create_order_view, name='create-order'),
    path('<int:pk>/', order_detail_view, name='order-detail'),
    path('print_order_history/', print_order_history, name='print_order_history'),
]
