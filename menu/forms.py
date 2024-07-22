from django import forms
from .models import menuItem, Restaurant
from django.contrib.auth.models import User

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = menuItem
        fields = ['name', 'category', 'price']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the 'user' parameter from kwargs
        super(MenuItemForm, self).__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            self.fields['restaurant'].initial = user.restaurant  # Assuming user.restaurant is the related restaurant instance

    def save(self, commit=True):
        instance = super(MenuItemForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name']


class RestaurantSelectForm(forms.Form):
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), label="Select Restaurant")