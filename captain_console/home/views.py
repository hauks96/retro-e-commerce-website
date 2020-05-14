from django.shortcuts import render
from shop.models import Category
from .models import BannerImages


# Create your views here.
def home(request):
    """Displays the homepage of the website"""
    banner_images = BannerImages.objects.all()
    banner_images_ret = []
    for image in banner_images:
        if image.product.enabled:
            banner_images_ret.append(image)

    context = {'bannerImages': banner_images_ret,
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
    """Displays the website affiliate page"""
    return render(request, 'home/affiliate_page.html')


def shipping(request):
    """Displays the website shipping price page"""
    return render(request, 'home/shipping.html')
