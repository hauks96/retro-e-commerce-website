from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Address
from cart.models import Cart
from django.forms import widgets


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
        fields = ['email', 'first_name', 'last_name']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['id', ]
        fields = ['address', 'country', 'city', 'postal_code', 'note']


class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'username', 'password',
                   'email', 'first_name', 'last_name', 'enabled', 'address', 'cart', 'user_permissions', 'groups']
        widgets = {
            'image': widgets.URLInput(attrs={'class': 'form-control'}, ),
        }
