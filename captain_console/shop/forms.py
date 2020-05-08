from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from shop.models import Category


class AddToCart(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    product_quantity = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)],
                                          widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number',
                                                                          'min': 1, 'max': 50, 'step': 1}))


class Categories(forms.Form):
    allCategories = Category.objects.all()
    choices = [('All', 'All')]
    for category in allCategories:
        choices.append((category.getName(), category.getName()))
    categories = forms.ChoiceField(widget=forms.RadioSelect,
                                   choices=choices,
                                   initial=["All"])


class Filtering(forms.Form):
    order_by = forms.ChoiceField(widget=forms.RadioSelect,
                                 choices=[("name", "Name A-Z"),
                                          ("-name", "Name Z-A"),
                                          ("-price", "Price (high to low)"),
                                          ("price", "Price (low to high)")
                                          ],
                                 required=False)
