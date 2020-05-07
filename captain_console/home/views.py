from django.shortcuts import render
from shop.models import Category
from .models import BannerImages


# Create your views here.
# home page view (index)
def home(request):
    context = {'bannerImages': BannerImages.objects.all(),
               'productTypes': Category.objects.all().order_by('name')
               }
    return render(request, 'home/home.html', context)


def affiliate(request):
    return render(request, 'home/affiliatePage.html')

def shipping(request):
    return render(request, 'home/shipping.html')
