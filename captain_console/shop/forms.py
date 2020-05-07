from cart.models import CartItem
from django import forms

from shop.models import Category


class AddToCart(forms.ModelForm):
    product_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = CartItem
        fields = ['product_quantity', 'product_id']


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
