from django import forms
from .models import menuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = menuItem
        fields = ['name', 'category', 'price']
