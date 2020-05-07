from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms


class EditCartItem(forms.Form):
    product_id = forms.IntegerField(disabled=True, label='ID', widget=forms.HiddenInput())

    name = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    price = forms.FloatField(disabled=True, label='Unit Price',
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))

    quantity = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)],
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': 1, 'max': 50, 'step': 1}))

    total_price = forms.FloatField(disabled=True, label='Total Price (€)',
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    image = forms.CharField(max_length=999, widget=forms.HiddenInput(), disabled=True)
    is_remove = forms.BooleanField(widget=forms.HiddenInput(), disabled=True)
    is_edit = forms.BooleanField(widget=forms.HiddenInput(), disabled=True)

