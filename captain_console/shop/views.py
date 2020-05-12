from django.shortcuts import render, get_object_or_404, redirect
from shop.forms import AddToCart, Filtering, Categories
from shop.models import Product, ProductImage, Tag
from user.models import UserHistory
from time import gmtime, strftime
from django.db import IntegrityError


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
    try:
        request.COOKIES['cart']
        request.COOKIES['itm_count']
    except KeyError:
        response.set_cookie('cart', "")
        response.set_cookie('itm_count', 0)

    return response


def product(request, product_id):
    if request.method == 'GET':
        instance = get_object_or_404(Product, pk=product_id)
        if request.user.is_authenticated:  # add to search history
            UserHistory.objects.update_or_create(
                    user=request.user,
                    product=instance,
                    defaults={'date': strftime("%Y-%m-%d %H:%M:%S", gmtime())}
                )

        images = ProductImage.objects.filter(product_id=product_id)
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
                                                     'images': images,
                                                     'tags': tags,
                                                     'finalPrice': finalPrice,
                                                     'relatedProducts': relatedProducts})


def add_to_basket(request):
    """Cart items in cookie are stored as prod_id: quantity"""
    if request.method == "POST":
        form = AddToCart(data=request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['product_quantity']
            product_id = form.cleaned_data['product_id']

            # trying to fetch cookie from request
            try:
                cookie_cart = request.COOKIES['cart']
                cookie_item_counter = request.COOKIES['itm_count']
            except KeyError:
                #  If cookie does not exist yet, set cookie default to empty string
                cookie_cart = ""
                cookie_item_counter = 0

            cookie_item_counter = int(cookie_item_counter)
            cookie_item_counter += int(quantity)
            if cookie_cart == "":
                cart_dict = {str(product_id): int(quantity)}

            #  If there is content in the cookie string we create a dictionary from it's content
            else:
                cart_dict = render_dict_cookie(cookie_cart)
                # If item already in basket, add quantity
                if str(product_id) in cart_dict:
                    cart_dict[str(product_id)] += quantity
                    curr_quantity = cart_dict[str(product_id)]
                    cart_dict[str(product_id)] = str(curr_quantity)
                # Otherwise just add the key and value to the dictionary
                else:

                    cart_dict[str(product_id)] = str(quantity)

            # Adding new cookie to response and returning
            cookie_string = render_string_cookie(cart_dict)
            response = redirect('/shop/' + str(product_id) + '/')
            response.set_cookie('cart', cookie_string)
            response.set_cookie('itm_count', cookie_item_counter)

            return response


def render_dict_cookie(cookie_cart):
    """Converts cookie to dictionary object.
    To get cookie, try: request.COOKIES['cart'] except KeyError\n
    Dictionary keys in returned dictionary are STRINGS representing the product id \n
    Key value pairs are INTEGERS representing the corresponding product quantity"""
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
    """Converts the cookie dictionary created in render_dict_cookie method back to a string to set as cookie value\n
    ALWAYS USE THIS METHOD WHEN SETTING CART COOKIE\n
    The cookie fetched from browser is a string. Cart items in cookie are stored as product_id: quantity"""
    cart_product_ids = list(cart_dict.keys())
    cookie_string = ""
    for i in range(len(cart_product_ids)):
        cookie_string += cart_product_ids[i] + ":" + str(cart_dict[cart_product_ids[i]]) + " "

    return cookie_string

