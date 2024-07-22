from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import customer_view, create_customer_view, customer_detail_view
from django.conf.urls import handler403

urlpatterns = [
    path('', customer_view, name='customer-view'),
    path('create/', create_customer_view, name='create-customer'),
    path('<int:pk>/', customer_detail_view, name='customer-detail'),
]

handler403 = 'order.views.handler403'