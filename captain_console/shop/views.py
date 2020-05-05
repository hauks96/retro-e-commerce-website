from django.shortcuts import render
from shop.models import Product, ProductImage


# Create your views here.

def shop(request):
    if 'search_filter' in request:
        # filter by search filter
        pass
    elif 'product_type' in request:
        # filter by product type
        pass
    elif 'by_name' in request:
        # filter by name value asc/desc
        pass
    else:
        # return all data
        pass
    products = Product.objects.all()
    # dump images into product collection
    # we only want the first image we find
    images = {}
    for item in products:
        #print(item.id)
        images[item] = ProductImage.objects.filter(product_id=item.id).first()

    print(images)
    products = images
    context = {"products": products}
    return render(request, 'shop/shop.html', context)


def product(request, product_id):
    # fetch product data or return 404
    # if user.is_authenticated -> save search to search hisory model
    # load product details page
    return render(request, 'shop/product.html')
