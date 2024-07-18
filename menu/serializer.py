from rest_framework import serializers
from .models import menuItem

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = menuItem
        fields = '__all__'