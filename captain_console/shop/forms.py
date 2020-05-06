from cart.models import CartItem
from django import forms


class AddToCart(forms.ModelForm):
    product_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = CartItem
        fields = ['product_quantity', 'product_id']