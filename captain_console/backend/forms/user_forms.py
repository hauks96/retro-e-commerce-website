from django.forms import ModelForm, widgets
from user.models import Address, User
# Create your views here.


class userCreateForm(ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'last_login', 'is_superuser', 'is_active', 'date_joined', 'groups', 'user_permissions', 'address']
        widgets = {
            'username': widgets.TextInput(attrs={'class': 'form-control'}),
            'password': widgets.PasswordInput(attrs={'class': 'form-control'}),
            'email': widgets.EmailInput(attrs={'class': 'form-control'}),
            'first_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'last_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'image': widgets.URLInput(attrs={'class': 'form-control'}),
            'enabled': widgets.NullBooleanSelect(attrs={'class': 'form-control'}),
            # Add option to create staff or superuser?

        }

class userUpdateForm(ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'last_login', 'is_superuser', 'is_active', 'date_joined',
                   'groups', 'user_permissions', 'address', 'username']
        widgets = {
            'password': widgets.PasswordInput(attrs={'class': 'form-control'}),
            'email': widgets.EmailInput(attrs={'class': 'form-control'}),
            'first_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'last_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'image': widgets.URLInput(attrs={'class': 'form-control'}),
            'enabled': widgets.NullBooleanSelect(attrs={'class': 'form-control'}),
            # Add option to create staff or superuser?

        }
