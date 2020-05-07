from django.forms import ModelForm, widgets
from django import forms
from user.models import Address
from django.db import models


class ShippingAddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['id']
        widgets = {
            'address': widgets.TextInput(attrs={'class': 'form-control'}),
            'country': widgets.TextInput(attrs={'class': 'form-control'}),
            'city': widgets.TextInput(attrs={'class': 'form-control'}),
            'postal_code': widgets.TextInput(attrs={'class': 'form-control'}),
            'note': widgets.TextInput(attrs={'class': 'form-control'}),
        }


class PaymentInfoForm(forms.Form):
    cardholder_name = forms.CharField(label='Please enter cardholder name', max_length=20, required=True),
    credit_card_num = forms.CharField(label='Please enter your credit card number', max_length=20, required=True),
    expiry_date = forms.NumberInput()
    CVC = forms.NumberInput()





