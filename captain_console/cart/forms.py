from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms


class EditCartItem(forms.Form):
    product_id = forms.IntegerField(label='ID', widget=forms.HiddenInput())

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    price = forms.FloatField(label='Unit Price',
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))

    quantity = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)],
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': 1, 'max': 50, 'step': 1}))

    total_price = forms.FloatField(label='Total Price (€)',
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    image = forms.CharField(max_length=999, widget=forms.HiddenInput())

    remove = forms.CharField(widget=forms.HiddenInput())
    edit = forms.CharField(widget=forms.HiddenInput())

