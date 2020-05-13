from django.http import HttpResponse
from django.shortcuts import render
from shop.models import Category
from .models import BannerImages
from shop.views import render_dict_cookie

# Create your views here.
# home page view (index)
def home(request):
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
    return render(request, 'home/affiliatePage.html')

def shipping(request):
    return render(request, 'home/shipping.html')