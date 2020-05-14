from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.widgets import CountrySelectWidget
from .models import User, Address
from django.forms import widgets


class UserRegistrationForm(UserCreationForm):
    username = forms.Field(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.Field(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.Field(label='Password',
                            required=True,
                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.Field(label='Password Confirmation',
                            required=True,
                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.Field(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.Field(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        exclude = ['id', 'enabled', 'address', 'image']
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

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
