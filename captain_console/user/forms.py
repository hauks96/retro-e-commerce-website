from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Address
from cart.models import Cart


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        exclude = ['id', 'enabled', 'address', 'image', 'cart']
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user_cart = Cart()
        user_cart.save()
        user_address = Address()
        user_address.save()
        user.address = user_address
        user.cart = user_cart

        if commit:
            user.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'enabled', 'cart']
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'image']
