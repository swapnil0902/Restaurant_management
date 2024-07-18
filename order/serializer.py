from rest_framework import serializers
from .models import Order
from customer.models import Customer
from customer.serializer import CustomerSerializer
from menu.models import menuItem
from menu.serializer import MenuSerializer


class OrderSerializer(serializers.ModelSerializer):
    menu_id = serializers.PrimaryKeyRelatedField(queryset=menuItem.objects.all())
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    menu_name = serializers.CharField(source='menu_id.name', read_only=True)
    customer_name = serializers.CharField(source='customer_id.name', read_only=True)
    rate = serializers.DecimalField(max_digits=10, decimal_places=2, source='menu_id.price', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'menu_id', 'menu_name', 'customer_id', 'customer_name', 'quantity', 'rate', 'total_price')
        read_only_fields = ('menu_name', 'customer_name', 'rate', 'total_price') 

    def create(self, validated_data):
        menu_id = validated_data.pop('menu_id')
        customer_id = validated_data.pop('customer_id')
        rate = menu_id.price
        order = Order.objects.create(menu_id=menu_id, customer_id=customer_id, rate = rate, **validated_data)
        return order

    def update(self, instance, validated_data):
        menu_id = validated_data.pop('menu_id')
        customer_id = validated_data.pop('customer_id')
        instance.menu_id = menu_id
        instance.customer_id = customer_id
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()
        return instance