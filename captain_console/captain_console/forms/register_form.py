from django.contrib.auth.forms import UserCreationForm
from django import forms
from user.models import User


class UserCreateForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        exclude = ['id', 'enabled', 'address', 'image', 'cart']
        fields = ['username', 'email', 'password1', 'password2', 'firstName', 'lastName']
