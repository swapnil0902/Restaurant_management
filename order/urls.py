from django.urls import path
from .views import order_view, create_order_view, order_detail_view, print_order_history, handler403
from django.conf.urls import handler403


urlpatterns = [
    path('', order_view, name='order-view'),
    path('create/', create_order_view, name='create-order'),
    path('create/<int:restaurant_id>/', create_order_view, name='create-order-restaurant'),
    path('<int:pk>/', order_detail_view, name='order-detail'),
    path('print_order_history/', print_order_history, name='print_order_history'),
]
# handler403 = 'order.views.handler403'