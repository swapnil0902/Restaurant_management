# serializers.py

from rest_framework import serializers
from .models import menuItem, Restaurant, User

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = menuItem
        fields = ('id', 'name', 'category', 'price', 'restaurant')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def create(self, validated_data):
        return menuItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'owner', 'name', 'email', 'menu_items')

    def create(self, validated_data):
        menu_items_data = validated_data.pop('menu_items', [])
        restaurant = Restaurant.objects.create(**validated_data)
        for menu_item_data in menu_items_data:
            menuItem.objects.create(restaurant=restaurant, **menu_item_data)
        return restaurant

    def update(self, instance, validated_data):
        menu_items_data = validated_data.pop('menu_items', [])
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        existing_menu_items = instance.menu_items.all()
        existing_menu_items_ids = [item.id for item in existing_menu_items]

        for menu_item_data in menu_items_data:
            menu_item_id = menu_item_data.get('id', None)
            if menu_item_id in existing_menu_items_ids:
                menu_item = menuItem.objects.get(id=menu_item_id)
                menu_item.name = menu_item_data.get('name', menu_item.name)
                menu_item.category = menu_item_data.get('category', menu_item.category)
                menu_item.price = menu_item_data.get('price', menu_item.price)
                menu_item.save()
            else:
                menuItem.objects.create(restaurant=instance, **menu_item_data)

        return instance
