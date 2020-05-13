from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.widgets import CountrySelectWidget
from .models import User, Address
from django.forms import widgets


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        exclude = ['id', 'enabled', 'address', 'image']
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'username': widgets.TextInput(attrs={'class': 'form-control'}),
            'email': widgets.TextInput(attrs={'class': 'form-control'}),
            'password1': widgets.TextInput(attrs={'class': 'form-control'}),
            'password2': widgets.TextInput(attrs={'class': 'form-control'}),
            'first_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'last_name': widgets.TextInput(attrs={'class': 'form-control'})
        }
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user_address = Address()
        user_address.save()
        user.address = user_address

        if commit:
            user.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'enabled']
        fields = ['email', 'first_name', 'last_name']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['id', ]
        fields = ['full_name', 'address', 'country', 'city', 'postal_code', 'note']
        widgets = {'country': CountrySelectWidget()}


class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'username', 'password',
                   'email', 'first_name', 'last_name', 'enabled', 'address', 'user_permissions', 'groups']
        widgets = {
            'image': widgets.URLInput(attrs={'class': 'form-control'}, ),
        }
