from django.forms import ModelForm, widgets
from home.models import BannerImages


class carouselImageForm(ModelForm):

    class Meta:
        model = BannerImages
        exclude = ['id']
        widgets = {
            'imageURL': widgets.URLInput(attrs={'class': 'form-control'}),
            'product': widgets.Select(attrs={'class': 'form-control'})
        }