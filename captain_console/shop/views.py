from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import json

from shop.forms import AddToCart, Filtering, Categories
from user.models import User
from cart.models import CartItem
from shop.models import Product, ProductImage, Tag


# Create your views here.


def shop(request):
    # filtering is dynamic except for the 'All' category.
    if 'categories' in request.GET and 'order_by' in request.GET:
        if request.GET['categories'] == 'All':
            products = Product.objects.all().order_by(request.GET['order_by'])
        else:
            products = Product.objects.filter(
                category__name__contains=request.GET['categories']
            ).order_by(
                request.GET['order_by'])
    elif 'categories' in request.GET:
        if request.GET['categories'] == 'All':
            products = Product.objects.all()
        else:
            products = Product.objects.filter(category__name__contains=request.GET['categories'])
    elif 'order_by' in request.GET:
        products = Product.objects.all().order_by(request.GET['order_by'])
    else:
        products = Product.objects.all()

    if len(products) == 0:  # failsafe in case user messes with url parameters
        products = Product.objects.all()
    # dump images into product collection, we only want the first image we find,
    # and calculate a final price
    temp = {}
    finalPrice = {}
    for item in products:
        temp[item] = (ProductImage.objects.filter(product_id=item.id).first(), item.getFinalPrice())
        if temp[item] is None:  # if no image is found
            temp[item] = "static/images/no-image-found.png"  # default.

    products = temp
    filters = Filtering()
    categories = Categories()
    context = {"products": products,
               "filters": filters,
               "categories": categories}
    response = render(request, 'shop/shop.html', context)
    if 'cart' not in request.COOKIES:
        response.set_cookie('cart', "")

    return response


def product(request, product_id):
    # if user.is_authenticated -> save search to search history model
    # load product details page
    # todo: add to search history if authenticated
    if request.method == 'GET':

        instance = get_object_or_404(Product, pk=product_id)
        image = ProductImage.objects.filter(product_id=product_id).first()
        tags = Tag.objects.filter(product_id=product_id)
        relatedProducts = []
        # todo: make a better searcher for related tags
        for count, tag in enumerate(tags):
            innerList = []
            if count == 5:  # we dont want more than 5 items
                break
            innerList.append(Product.objects.filter(tag__tag__icontains=tag))
            # get pictures of related products
            innerList.append(ProductImage.objects.filter(product_id=innerList[0][0].pk).first())
            relatedProducts.append(innerList)

        # calculate discounted price
        if instance.discount == 0:
            finalPrice = instance.price
        else:
            finalPrice = instance.price * (100 - instance.discount) / 100

        form = AddToCart(initial={'product_quantity': 1, 'product_id': product_id})

        return render(request, 'shop/product.html', {'form': form,
                                                     'product': instance,
                                                     'image': image,
                                                     'tags': tags,
                                                     'finalPrice': finalPrice,
                                                     'relatedProducts': relatedProducts})


def add_to_basket(request):
    """Cart items in session are stored as prod_id: quantity"""
    if request.method == "POST":
        form = AddToCart(data=request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['product_quantity']
            product_id = form.cleaned_data['product_id']
            current_product = Product.objects.get(id=product_id)
            """
            if request.user.is_authenticated:
                user = User.objects.get(id=request.user.id)
                cart = user.cart
                try:
                    cart_item = CartItem.objects.get(product=product_id, cart=cart.id)
                    cart_item.product_quantity += 1
                except CartItem.DoesNotExist:
                    cart_item = CartItem(product=current_product.id, quantity=quantity, cart=cart.id)
                cart_item.save()
                response = redirect('/shop/' + str(product_id) + '/')
            else:
            """
            #  User is not logged so we add his cart items to a cookie called cart
            try:
                cookie_cart = request.COOKIES['cart']
            except KeyError:
                #  If cookie does not exist yet set default to empty string
                cookie_cart = ""

            if cookie_cart == "":
                cart_dict = {str(product_id): int(quantity)}

            #  If there is content in the cookie string we create a dictionary from it's content
            else:
                cart_dict = render_dict_cookie(cookie_cart)
                if str(product_id) in cart_dict:
                    cart_dict[str(product_id)] += quantity
                    curr_quantity = cart_dict[str(product_id)]
                    cart_dict[str(product_id)] = str(curr_quantity)
                else:

                    cart_dict[str(product_id)] = str(quantity)

            cookie_string = render_string_cookie(cart_dict)
            response = redirect('/shop/' + str(product_id) + '/')
            response.set_cookie('cart', cookie_string)

            return response


def render_dict_cookie(cookie_cart):
    """Converts cookie to dictionary object.
    key being a string representing the product id
    value being an integer representing the product quantity"""
    cookie_items = cookie_cart.split(' ')
    cart_dict = {}

    for item in cookie_items:
        if not item:
            del item
        else:
            curr_item = item.split(":")
            cart_dict[curr_item[0]] = int(curr_item[1])

    return cart_dict


def render_string_cookie(cart_dict):
    """Converts the cookie dictionary created in render_dict_cookie method back to a string to set as cookie value"""
    cart_product_ids = list(cart_dict.keys())
    cookie_string = ""
    for i in range(len(cart_product_ids)):
        cookie_string += cart_product_ids[i] + ":" + str(cart_dict[cart_product_ids[i]]) + " "

    return cookie_string

