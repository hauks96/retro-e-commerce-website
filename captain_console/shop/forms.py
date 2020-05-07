from cart.models import CartItem
from django import forms

from shop.models import Category


class AddToCart(forms.ModelForm):
    product_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = CartItem
        fields = ['product_quantity', 'product_id']


class Categories(forms.Form):
    # todo: dynamically get all categories from the Category model, change views accordingly(lot of work)
    categories = forms.ChoiceField(widget=forms.RadioSelect,
                                   choices=[("All", "All"),
                                            (1, "Console"),
                                            (2, "Games"),
                                            (3, "Other")
                                            ],
                                   initial=["All"])


class Filtering(forms.Form):
    filter_by = forms.ChoiceField(widget=forms.RadioSelect,
                                  choices=[("nameAsc", "Name A-Z"),
                                           ("nameDesc", "Name Z-A"),
                                           ("priceDesc", "Price (high to low)"),
                                           ("priceAsc", "Price (low to high)")
                                           ],
                                  required=False)
