from django.shortcuts import render
from shop.models import Product #importar products
# Create your views here.

def shop(request):
    if 'search_filter' in request:
        #filter by search filter
        pass
    elif 'product_type' in request:
        #filter by product type
        pass
    elif 'by_name' in request:
        #filter by name value asc/desc
        pass
    else:
        #return all data
        pass

    return render(request, 'shop/shop.html', context={"products": Product.objects.all()})

def product(request, product_id):
    #fetch product data or return 404
    #if user.is_authenticated -> save search to search hisory model
    #load product details page
    return render(request, 'shop/product.html')
