from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from user.models import User


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(label="Email", help_text=False)
    username = forms.CharField(label="Username", help_text="")

    class Meta:
        model = User
        exclude = ['id', 'enabled', 'address', 'image', 'cart']
        fields = ['username', 'email', 'password1', 'password2', 'firstName', 'lastName']
