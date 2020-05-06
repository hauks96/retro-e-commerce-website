from cart.models import CartItem
from django import forms


class AddToCart(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product_quantity']