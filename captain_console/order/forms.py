from django.forms import ModelForm, widgets
from django import forms
from user.models import Address
from order.models import Order
from django.db import models


class ShippingAddressForm(ModelForm):  # To use if user is logged in and wants to use his saved address info
    address_email = forms.EmailField(required=True)
    class Meta:
        model = Address
        exclude = ['id']
        widgets = {
            'full_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'address': widgets.TextInput(attrs={'class': 'form-control'}),
            'country': widgets.TextInput(attrs={'class': 'form-control'}),
            'city': widgets.TextInput(attrs={'class': 'form-control'}),
            'postal_code': widgets.TextInput(attrs={'class': 'form-control'}),
            'note': widgets.TextInput(attrs={'class': 'form-control'}),
        }


class ShippingAddressInfoForm(forms.Form):
    address_email = forms.EmailField(required=True)
    full_name = forms.CharField(label='Full name', max_length=70, required=True)
    address = forms.CharField(label='Address', max_length=32, required=True)
    country = forms.CharField(label='Country', max_length=32, required=True)
    city = forms.CharField(label='City', max_length=32, required=True)
    postal_code = forms.CharField(label='Postal Code', max_length=12, required=True)
    note = forms.CharField(label='Enter additional info if required', max_length=100, required=False)



class PaymentInfoForm(forms.Form):
    # If forms.NumberInput() is used the form does not show on the template
    cardholder_name = forms.CharField(label='Cardholder name', max_length=26, required=True,
                                      widget=forms.TextInput(attrs={'placeholder': 'John Doe'}))
    credit_card_num = forms.CharField(label='Credit card number', max_length=100, required=True,
                                      widget=forms.TextInput(attrs={'placeholder': '1234-1234-1234-1234'}))
    expiry_year = forms.ChoiceField(choices=[('', '------'), ('20', '2020'), ('21', '2021'), ('22', '2022'),
                                             ('23', '2023'), ('24', '2024'), ('25', '2025'), ('26', '2026')])
    expiry_month = forms.ChoiceField(choices=[('', '---------'), ('01', 'January'), ('02', 'February'), ('03', 'March'),
                                              ('04', 'April',), ('05', 'May'), ('06', 'June'), ('07', 'July'),
                                              ('08', 'August'), ('09', 'September'), ('10', 'October'),
                                              ('11', 'November'), ('12', 'December')], label='Card expiry date',
                                     required=True,
                                     help_text='enter card expiry date with a slash in between, f.x: "01/21"')
    CVC = forms.CharField(label='3 digit CVC number', max_length=3,
                          required=True, help_text='Please enter 3 digit CVC number on the back of your card')

    def clean_credit_card_num(self):
        credit_card_num = self.cleaned_data.get("credit_card_num")
        if len("".join(credit_card_num.split("-"))) != 16:
            raise forms.ValidationError("Please enter a valid credit card number")
        if not "".join(credit_card_num.split("-")).isdigit():  # If the number does not contain all digits
            raise forms.ValidationError("Credit card number must only contain numbers and dashes.")
        return credit_card_num

    """
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get("expiry_date")
        if len(expiry_date) != 5:
            raise forms.ValidationError("Please enter your card expiry date with a slash in between")
        elif "/" not in expiry_date:
            raise forms.ValidationError("Please enter your card expiry date with a slash in between")
        return expiry_date
    """

    def clean_CVC(self):
        CVC = self.cleaned_data.get("CVC")
        if len(CVC.strip()) != 3:
            raise forms.ValidationError("Please enter your 3 digit CVC number found on the back of your card")
        return CVC


class CartItemDisplay(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(label='Unit Price', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    total_price = forms.FloatField(label='Total Price (€)',
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.CharField(max_length=999, widget=forms.HiddenInput())


