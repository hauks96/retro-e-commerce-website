from django.shortcuts import render
from shop.models import Category
from .models import BannerImages


# Create your views here.
# home page view (index)
def home(request):
    request.session.set_test_cookie()
    context = {'bannerImages': BannerImages.objects.all(),
               'productTypes': Category.objects.all().order_by('name')
               }
    return render(request, 'home/home.html', context)
