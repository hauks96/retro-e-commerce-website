from django.forms import ModelForm, widgets
from django import forms
from shop.models import Product, Category, ProductImage, Tag


class productCreateForm(ModelForm):
    image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        exclude = ['id', 'tag']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control'}),
            'enabled': widgets.NullBooleanSelect(attrs={'class': 'form-control'}).is_required,
            'discount': widgets.NumberInput(attrs={'class': 'form-control'}),
            'short_description': widgets.TextInput(attrs={'class': 'form-control'}),
            'long_description': widgets.Textarea(attrs={'class': 'form-control'}),
            'category': widgets.Select(attrs={'class': 'form-control'}),
        }


class productUpdateForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['id', 'tag']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control'}),
            'enabled': widgets.NullBooleanSelect(attrs={'class': 'form-control'}).is_required,
            'discount': widgets.NumberInput(attrs={'class': 'form-control'}),
            'short_description': widgets.TextInput(attrs={'class': 'form-control'}),
            'long_description': widgets.Textarea(attrs={'class': 'form-control'}),
            'category': widgets.Select(attrs={'class': 'form-control'}),
        }


class singleTag(ModelForm):
    class Meta:
        model = Tag
        exclude = ['id']
        widgets = {
            'tag': widgets.TextInput(attrs={'class': 'form-control'}),
        }


class selectTagForm(forms.Form):
    tag = forms.ModelChoiceField(queryset=Tag.objects.all())


class singleImage(ModelForm):
    class Meta:
        model = ProductImage
        exclude = ['id']
        widgets = {
            'image': widgets.URLInput(attrs={'class': 'form-control'}),
            'product': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }


class categoryCreateForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['id']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'image': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
        }


class categoryDeleteForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
