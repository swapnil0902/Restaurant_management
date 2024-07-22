from rest_framework import serializers
from .models import Order
from customer.models import Customer
from menu.models import menuItem  # Corrected import name
from customer.serializer import CustomerSerializer  # Corrected import name
from menu.serializer import MenuSerializer  # Corrected import name

class OrderSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=menuItem.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    menu_name = serializers.CharField(source='menu_id.name', read_only=True)
    customer_name = serializers.CharField(source='customer_id.name', read_only=True)
    rate = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'menu_item', 'menu_name', 'customer', 'customer_name', 'quantity', 'rate', 'total_price')
        read_only_fields = ('menu_name', 'customer_name', 'rate', 'total_price')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rate'] = instance.menu_item.price  # Fetch price from related MenuItem
        return representation

    def create(self, validated_data):
        menu_id = validated_data.pop('menu_item')
        customer_id = validated_data.pop('customer')
        rate = menu_id.price  # Assuming menu_id is an instance of MenuItem
        total_price = validated_data.get('quantity', 0) * rate  # Calculate total_price
        order = Order.objects.create(menu_id=menu_id, customer_id=customer_id, rate=rate, total_price=total_price, **validated_data)
        return order

    def update(self, instance, validated_data):
        menu_id = validated_data.pop('menu_item')
        customer_id = validated_data.pop('customer')
        instance.menu_id = menu_id
        instance.customer_id = customer_id
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.rate = menu_id.price  # Update rate based on new menu_id price
        instance.total_price = instance.quantity * instance.rate  # Recalculate total_price
        instance.save()
        return instance
