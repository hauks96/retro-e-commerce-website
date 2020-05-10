from django.forms import ModelForm, widgets
from django import forms
from user.models import Address
from django.db import models


class ShippingAddressForm(ModelForm):  # To use if user is logged in and wants to use his saved address info
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
    country = forms.CharField(label='Please enter your Country', max_length=56, required=True)
    city = forms.CharField(label='Please enter your City', max_length=100, required=True)
    postal_code = forms.CharField(label='Please enter your Postal Code', max_length=10, required=True)
    note = forms.CharField(label='Enter additional info if required', max_length=25, required=False)


class PaymentInfoForm(forms.Form):
    # If forms.NumberInput() is used the form does not show on the template
    cardholder_name = forms.CharField(label='Please enter cardholder name', max_length=26, required=True)
    credit_card_num = forms.CharField(label='Please enter credit card number', max_length=100, required=True)
    expiry_date = forms.CharField(label='Please enter card expiry date with a slash in between, f.x: "01/21"',
                                  max_length=100, required=True)
    CVC = forms.CharField(label='Please enter 3 digit CVC number on the back of your card', max_length=100,
                          required=True)

    def clean_credit_card_num(self):
        credit_card_num = self.cleaned_data.get("credit_card_num")
        if len(credit_card_num.strip('-')) != 16:
            raise forms.ValidationError("Please enter a valid credit card number")
        if not "".join(credit_card_num.split("-")).isdigit():  # If the number does not contain all digits
            raise forms.ValidationError("Please enter a valid credit card number")
        return credit_card_num

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get("expiry_date")
        if len(expiry_date != 5):
            raise forms.ValidationError("Please enter your card expiry date with a slash in between")
        elif "/" not in expiry_date:
            raise forms.ValidationError("Please enter your card expiry date with a slash in between")
        return expiry_date

    def clean_CVC(self):
        CVC = self.cleaned_data.get("CVC")
        if len(CVC.strip()) is not 3:
            raise forms.ValidationError("Please enter your 3 digit CVC number found on the back of your card")
        return CVC


class CartItemDisplay(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(label='Unit Price', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    total_price = forms.FloatField(label='Total Price (€)',
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.CharField(max_length=999, widget=forms.HiddenInput())
