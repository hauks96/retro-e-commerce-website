from django.forms import ModelForm, widgets
from django import forms
from user.models import Address
from django.db import models


class ShippingAddressForm(ModelForm): #To use if user is logged in and wants to use his saved address info
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


class ShippingAddressInfoForm(forms.Form):
    address = forms.CharField(label='Please enter your Address', max_length=100, required=True)
    country = forms.CharField(label='Please enter your Country', max_length=50, required=True)
    city = forms.CharField(label='Please enter your City', max_length=50, required=True)
    postal_code = forms.CharField(label='Please enter your Postal Code', max_length=20, required=True)
    note = forms.CharField(label='Enter additional info if required', max_length=25, required=False)


class PaymentInfoForm(forms.Form):
    # If forms.NumberInput() is used the form does not show on the template
    cardholder_name = forms.CharField(label='Please enter cardholder name', max_length=100, required=True)
    credit_card_num = forms.CharField(label='Please enter credit card number', max_length=100, required=True)
    expiry_date = forms.CharField(label='Please enter expiry date', max_length=100, required=True)
    CVC = forms.CharField(label='Please enter 3 digit CVC number on the back of your card', max_length=100, required=True)






