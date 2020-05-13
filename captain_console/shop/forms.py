from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe

from shop.models import Category


class AddToCart(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    product_quantity = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)],
                                          widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number',
                                                                          'min': 1, 'max': 50, 'step': 1}))


def get_choices():
    allCategories = Category.objects.all()
    choices = []
    for category in allCategories:
        choices.append((category.getName(), category.getName()))
    return choices


class Categories(forms.Form):
    categories = forms.ChoiceField(label=mark_safe("<strong>Categories</strong>"), widget=forms.RadioSelect,
                                   choices=get_choices,
                                   initial=["All"])


class Filtering(forms.Form):
    order_by = forms.ChoiceField(label=mark_safe("<strong>Order by</strong>"), widget=forms.RadioSelect(attrs={
        'font-weight': 'bolder'}),
                                 choices=[("name", "Name A-Z"),
                                          ("-name", "Name Z-A"),
                                          ("-price", "Price (high to low)"),
                                          ("price", "Price (low to high)")
                                          ],
                                 required=False)


class SearchBar(forms.Form):
    search = forms.CharField(label=mark_safe('<strong>Search</strong>'),
                             required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
