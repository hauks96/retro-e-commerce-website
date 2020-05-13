from django.shortcuts import render
from shop.models import Category
from .models import BannerImages


# Create your views here.
# home page view (index)
def home(request):
    context = {'bannerImages': BannerImages.objects.all(),
               'productTypes': Category.objects.all().order_by('name')
               }
    response = render(request, 'home/home.html', context)
    try:
        cart_cookie = request.COOKIES['cart']
    # if it fails to fetch, there is no cookie, so we create a new empty cookie and return a response
    except KeyError:
        response.set_cookie('cart', "")
        response.set_cookie('itm_count', 0)

    return response


def affiliate(request):
    return render(request, 'home/affiliatePage.html')


def shipping(request):
    return render(request, 'home/shipping.html')
