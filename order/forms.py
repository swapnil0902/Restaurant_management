from django import forms
from .models import Order
from menu.models import Restaurant, menuItem
        
class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        restaurant = kwargs.pop('restaurant', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if restaurant:
            self.fields['menu_items'].queryset = menuItem.objects.filter(restaurant=restaurant)

    
    menu_items = forms.ModelMultipleChoiceField(
        queryset=menuItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Menu Items"
    )

    quantities = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        label="Enter Quantities (comma-separated)"
    )

    class Meta:
        model = Order
        fields = ['menu_items']


class RestaurantSelectionForm(forms.Form):
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), label="Select Restaurant")


class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['menu_item', 'quantity']  # Fields you want to include in the form
    
    def __init__(self, *args, **kwargs):
        restaurant = kwargs.pop('restaurant', None)
        super().__init__(*args, **kwargs)
        
        if restaurant:
            # Filter menu items by the restaurant
            self.fields['menu_item'].queryset = menuItem.objects.filter(restaurant=restaurant)