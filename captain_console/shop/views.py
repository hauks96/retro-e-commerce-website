from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import json

from shop.forms import AddToCart
from shop.models import Product, ProductImage
from user.models import User
from cart.models import CartItem
# Create your views here.



def shop(request):
    cookie_allowed = False
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        cookie_allowed = True
    else:
        return HttpResponse("Please enable cookies and try again.")
    context = {}
    data = []
    if 'search_filter' in request.GET:
        search = request.GET['search_filter']

        if 'by_name' in request.GET:
            by_name = request.GET['by_name']  # Asc or Desc
            if by_name == 'asc':
                data = Product.objects.filter(name__icontains=search).order_by('-name')
            else:
                data = Product.objects.filter(name__icontains=search).order_by('name')

        elif 'by_price' in request.GET:
            by_price = request.GET['by_price']  # Asc or Desc
            if by_price == 'asc':
                data = Product.objects.filter(name__icontains=search).order_by('-price')
            else:
                data = Product.objects.filter(name__icontains=search).order_by('price')

        else:
            data = Product.objects.filter(name__icontains=search)

    if 'product_type' in request.GET:
        prod_type = request.GET['product_type']
        if data:
            for item in data:
                if item.category != prod_type:
                    del item

        else:
            if 'by_name' in request.GET:
                by_name = request.GET['by_name']  # Asc or Desc
                if by_name == 'asc':
                    data = Product.objects.filter(category=prod_type).order_by('-name')
                else:
                    data = Product.objects.filter(category=prod_type).order_by('name')

            elif 'by_price' in request.GET:
                by_price = request.GET['by_price']  # Asc or Desc
                if by_price == 'asc':
                    data = Product.objects.filter(category=prod_type).order_by('-price')
                else:
                    data = Product.objects.filter(category=prod_type).order_by('price')

            else:
                data = Product.objects.filter(category=prod_type)

    elif 'by_name' in request.GET:
        by_name = request.GET['by_name']  # Asc or Desc
        if by_name == 'asc':
            data = Product.objects.all().order_by('-name')
        else:
            data = Product.objects.all().order_by('name')

    elif 'by_price' in request.GET:
        by_price = request.GET['by_price']  # Asc or Desc
        if by_price == 'asc':
            data = Product.objects.all().order_by('-price')
        else:
            data = Product.objects.all().order_by('price')

    else:
        data = Product.objects.all()

    """
    products = [{
        'id': x.id,
        'name': x.name,
        'category': x.category.name,
        'price': x.price,
        'image': ProductImage.objects.filter(product_id=x.id).first().image
    } for x in data]
    """

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
    response = render(request, 'shop/shop.html', context)
    if cookie_allowed:
        response.set_cookie('cart', {})
    return response




def product(request, product_id):
    # if user.is_authenticated -> save search to search history model
    # load product details page
    # todo: add to search history if authenticated
    if request.method == 'GET':
        instance = get_object_or_404(Product, pk=product_id)
        image = ProductImage.objects.filter(product_id=product_id).first()
        # calculate discounted price
        if instance.discount == 0:
            finalPrice = instance.price
        else:
            finalPrice = instance.price * (100-instance.discount)/100
        return render(request, 'shop/product.html', {'product': instance,
                                                     'image': image,
                                                     'finalPrice': finalPrice})


def add_to_basket(request, product_id):
    """Cart items in session are stored as prod_id: quantity"""
    current_product = Product.objects.get(product_id)
    if request.method == "POST":
        form = AddToCart(data=request.POST)
        if form.is_valid():
            quantity = form.cleaned_data('product_quantity')

            if request.user.is_authenticated:
                user = User.objects.get(id=request.user.id)
                cart_item = CartItem(product=current_product, quantity=quantity)
                cart = user.cart
                cart.add(cart_item)

            else:
                cookie_cart = request.session.get('cart')
                cart_dict = json.loads(cookie_cart)
                if product_id in cart_dict:
                    cart_dict[product_id] += quantity
                else:
                    cart_dict[product_id] = quantity

                request.session['cart'] = cart_dict

            return HttpResponseRedirect(reverse('product-index', args=product_id))
        return HttpResponseNotFound('<h1>A critical error occurred saving your item to basket</h1>')
