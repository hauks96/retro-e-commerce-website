from django.shortcuts import render
from shop.models import Product, ProductImage

# Create your views here.
from user.models import User


def shop(request):
    context = {}
    if 'search_filter' in request.GET:
        search = request.GET['search_filter']

        if 'by_name' in request.GET:
            by_name = request.GET['by_name']  # Asc or Desc
            if by_name == 'asc':
                context["products"] = Product.objects.filter(name__icontains=search).order_by('-name')
            else:
                context["products"] = Product.objects.filter(name__icontains=search).order_by('name')

        elif 'by_price' in request.GET:
            by_price = request.GET['by_price']  # Asc or Desc
            if by_price == 'asc':
                context["products"] = Product.objects.filter(name__icontains=search).order_by('-price')
            else:
                context["products"] = Product.objects.filter(name__icontains=search).order_by('price')

        else:
            context["products"] = Product.objects.filter(name__icontains=search)

    if 'product_type' in request.GET:
        prod_type = request.GET['product_type']
        if context:
            for item in context['product']:
                if item.type != prod_type:
                    del item

        else:
            if 'by_name' in request.GET:
                by_name = request.GET['by_name']  # Asc or Desc
                if by_name == 'asc':
                    context["products"] = Product.objects.filter(type=prod_type).order_by('-name')
                else:
                    context["products"] = Product.objects.filter(type=prod_type).order_by('name')

            elif 'by_price' in request.GET:
                by_price = request.GET['by_price']  # Asc or Desc
                if by_price == 'asc':
                    context["products"] = Product.objects.filter(type=prod_type).order_by('-price')
                else:
                    context["products"] = Product.objects.filter(type=prod_type).order_by('price')

            else:
                context['product'] = Product.objects.filter(type=prod_type)

    elif 'by_name' in request.GET:
        by_name = request.GET['by_name']  # Asc or Desc
        if by_name == 'asc':
            context['product'] = Product.objects.all().order_by('-name')
        else:
            context['product'] = Product.objects.all().order_by('name')

    elif 'by_price' in request.GET:
        by_price = request.GET['by_price']  # Asc or Desc
        if by_price == 'asc':
            context["products"] = Product.objects.all().order_by('-price')
        else:
            context["products"] = Product.objects.all().order_by('price')

    else:
        context['products'] = Product.objects.all()

    # todo: fix image getting after filtering has been configured.
    products = Product.objects.all()
    # dump images into product collection
    # we only want the first image we find
    temp = {}
    for item in products:
        temp[item] = ProductImage.objects.filter(product_id=item.id).first()
        if temp[item] is None:  # if no image is found
            temp[item] = "static/images/no-image-found.png"  # default.

    products = temp
    context = {"products": products}
    return render(request, 'shop/shop.html', context)


def product(request, product_id):
    # if user.is_authenticated -> save search to search history model
    # load product details page
    # todo: add to search history if authenticated

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        pass    # todo: reroute to 404 page
        return render(request, 'shop/product.html')

    image = ProductImage.objects.filter(product_id=product_id).first()
    context = {'product': product,
               'image': image
               }
    return render(request, 'shop/product.html', context)


def add_to_basket(request):
    pass
    """
    value = request.COOKIES.get('cart')
    if value is None:
        # Cookie is not set
        response = render(request, template_name='user/shop.html')

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        basket = user.cart
    """
