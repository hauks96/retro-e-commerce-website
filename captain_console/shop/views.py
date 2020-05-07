from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import json

from shop.forms import AddToCart, Filtering, Categories
from user.models import User
from cart.models import CartItem
from shop.models import Product, ProductImage, Tag


# Create your views here.


def shop(request):
    products = None  # namespace
    if 'filter_by' in request.GET:
        filter = request.GET['filter_by']
        if filter == "nameAsc":
            if 'categories' in request.GET:
                if request.GET['categories'] != 'All':
                    products = Product.objects.filter(category=request.GET['categories']).order_by('name')
                else:
                    products = Product.objects.all().order_by('name')
            else:
                products = Product.objects.all().order_by('name')
        elif filter == "nameDesc":
            if 'categories' in request.GET:
                if request.GET['categories'] != 'All':
                    products = Product.objects.filter(category=request.GET['categories']).order_by('-name')
                else:
                    products = Product.objects.all().order_by('-name')
            else:
                products = Product.objects.all().order_by('-name')
        elif filter == "priceAsc":
            if 'categories' in request.GET:
                if request.GET['categories'] != 'All':
                    products = Product.objects.filter(category=request.GET['categories']).order_by('price')
                else:
                    products = Product.objects.all().order_by('price')
            else:
                products = Product.objects.all().order_by('price')
        elif filter == "priceDesc":
            if 'categories' in request.GET:
                if request.GET['categories'] != 'All':
                    products = Product.objects.filter(category=request.GET['categories']).order_by('price')
                else:
                    products = Product.objects.all().order_by('-price')
            else:
                products = Product.objects.all().order_by('-price')
    else:
        if 'categories' in request.GET:
            if request.GET['categories'] != 'All':
                products = Product.objects.filter(category=request.GET['categories'])
            else:
                products = Product.objects.all()
        else:
            products = Product.objects.all()

    # todo: fix image getting after filtering has been configured.
    # dump images into product collection
    # we only want the first image we find
    temp = {}
    for item in products:
        temp[item] = ProductImage.objects.filter(product_id=item.id).first()
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
                try:
                    cookie_cart = request.COOKIES['cart']
                except KeyError:
                    cookie_cart = ""

                if cookie_cart == "":
                    cart_dict = {str(product_id): str(quantity)}

                else:
                    cookie_items = cookie_cart.split(' ')
                    cart_dict = {}

                    for item in cookie_items:
                        if not item:
                            del item
                        else:
                            curr_item = item.split(":")
                            cart_dict[curr_item[0]] = int(curr_item[1])

                    if str(product_id) in cart_dict:
                        cart_dict[str(product_id)] += quantity
                        curr_quantity = cart_dict[str(product_id)]
                        cart_dict[str(product_id)] = str(curr_quantity)
                    else:
                        cart_dict[str(product_id)] = str(quantity)

                cart_product_ids = list(cart_dict.keys())
                cookie_string = ""
                for i in range(len(cart_product_ids)):
                    cookie_string += cart_product_ids[i] + ":" + str(cart_dict[cart_product_ids[i]]) + " "

                #  return HttpResponse('<h1>' + str(cart_dict) + '</h1>')
                response = redirect('/shop/' + str(product_id) + '/')
                response.set_cookie('cart', cookie_string)

            return response
