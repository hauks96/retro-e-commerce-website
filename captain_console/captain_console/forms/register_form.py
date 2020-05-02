from django.forms import ModelForm, widgets
from django import forms
from user.models import User


class UserCreateForm(ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'address', 'image', 'cart', 'enabled']
        widgets = {
            'username': widgets.TextInput(attrs={'class': 'form-control'}),
            'firstName': widgets.TextInput(attrs={'class': 'form-control'}),
            'lastName': widgets.TextInput(attrs={'class': 'form-control'}),
            'email': widgets.TextInput(attrs={'class': 'form-control'}),
            'password': widgets.PasswordInput(attrs={'class': 'form-control'}),
        }
