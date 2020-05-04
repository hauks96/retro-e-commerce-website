from django.forms import ModelForm, widgets
from django import forms
from shop.models import Product

class productCreateForm(ModelForm):
    image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Product
        exclude = ['id']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control'}),
            'enabled': widgets.NullBooleanSelect(attrs={'class': 'form-control'}).is_required,
            'discount': widgets.NumberInput(attrs={'class': 'form-control'}),
            'short_description': widgets.TextInput(attrs={'class': 'form-control'}),
            'long_description': widgets.TextInput(attrs={'class': 'form-control'}),
            'category': widgets.Select(attrs={'class': 'form-control'})
        }


