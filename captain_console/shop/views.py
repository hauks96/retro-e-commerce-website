from django.contrib.messages import get_messages
from django.shortcuts import render, get_object_or_404, redirect
from shop.forms import AddToCart, Filtering, Categories, SearchBar
from shop.models import Product, ProductImage
from user.models import UserHistory
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib import messages


# Create your views here.


def shop(request):
    """Sends queries to the database depending on the search and filter options
    chosen by the user and then displays those results to the shop section of the website."""
    failsafe = False  # user feedback if nothing was found
    # filtering is dynamic except for the 'All' category.
    if 'categories' in request.GET and 'order_by' in request.GET:
        if request.GET['categories'] == 'All':
            if 'search' in request.GET:
                products = Product.objects.filter(enabled=True,
                                                  name__contains=request.GET['search']).order_by(request.GET['order_by'])
            else:
                products = Product.objects.filter(enabled=True).order_by(request.GET['order_by'])
        else:
            if 'search' in request.GET:
                products = Product.objects.filter(
                    enabled=True,
                    category__name__contains=request.GET['categories'],
                    name__icontains=request.GET['search']
                )
            else:
                products = Product.objects.filter(
                    enabled=True,
                    category__name__contains=request.GET['categories']
                ).order_by(
                    request.GET['order_by'])
    elif 'categories' in request.GET:
        if request.GET['categories'] == 'All':
            if 'search' in request.GET:
                products = Product.objects.filter(enabled=True, name__icontains=request.GET['search'])
            else:
                products = Product.objects.filter(enabled=True)
        else:
            if 'search' in request.GET:
                products = Product.objects.filter(enabled=True, category__name__contains=request.GET['categories'],
                                                  name__icontains=request.GET['search'])
            else:
                products = Product.objects.filter(enabled=True, category__name__contains=request.GET['categories'])
    elif 'order_by' in request.GET:
        if 'search' in request.GET:
            products = Product.objects.filter(enabled=True, name__icontains=request.GET['search']).order_by(
                request.GET['order_by']
            )
        else:
            products = Product.objects.filter(enabled=True).order_by(request.GET['order_by'])
    else:
        if 'search' in request.GET:
            products = Product.objects.filter(enabled=True, name__icontains=request.GET['search'])
        else:
            products = Product.objects.filter(enabled=True)

    if len(products) == 0:  # failsafe in case user messes with url parameters
        failsafe = True
        products = Product.objects.filter(enabled=True)

    filters = Filtering()
    categories = Categories()
    searchBar = SearchBar()

    paginator = Paginator(products, 12)  # Show 12 products per page.
    # 12 pages since its dividable by 4,3,2 meaning we have more flexibility with rows.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj,
               "filters": filters,
               "categories": categories,
               "searchBar": searchBar,
               "failsafe": failsafe}
    response = render(request, 'shop/shop.html', context)
    try:
        request.COOKIES['cart']
        request.COOKIES['itm_count']
    except KeyError:
        response.set_cookie('cart', "")
        response.set_cookie('itm_count', 0)

    return response


def product(request, product_id):
    """Gets the product information, images and tags and displays it on a single product page"""
    if request.method == 'GET':
        instance = get_object_or_404(Product, pk=product_id)
        if instance.enabled is False:
            raise Http404  # if the product is set to enabled=False we reroute to 404.html
        if request.user.is_authenticated:  # add search to search history is user is logged in
            UserHistory.objects.update_or_create(
                user=request.user,
                product=instance,
            )

        images = ProductImage.objects.filter(product_id=product_id)  # Gets the relevant product images
        this_product = Product.objects.get(id=product_id)  # Get the product instance to be shown
        tags = this_product.tag.all()  # Gets the tags for this product
        relatedProducts = []  # Creates list of related products to display based on the tags
        count = 0
        tagnames = []
        for tag in tags:
            tagnames.append(tag.tag.lower())

        for cnt, tag in enumerate(tags):
            if count == 4:  # we dont want more than 5 items
                if this_product.get_category_name().lower() in tagnames[cnt:]:
                    index_of_tag = tagnames.index(this_product.get_category_name().lower())
                    the_tag = tags[index_of_tag]
                    current_products = the_tag.product_set.all()[:4]
                    for x in range(len(current_products)):
                        if current_products[x].id == product_id:
                            continue
                        else:
                            relatedProducts[x] = current_products[x]
                    break

            current_products = tag.product_set.all()[:4]
            for i in range(len(current_products)):
                if current_products[i].id == product_id:
                    continue
                else:
                    if count == 4:
                        break
                    relatedProducts.append(current_products[i])  # Connects the relevant products to the product
                    count += 1

        # calculate discounted price
        if instance.discount == 0:  # If there is no discount
            finalPrice = instance.price
        else:  # If discount
            finalPrice = instance.price * (100 - instance.discount) / 100  # Calculates the discount

        form = AddToCart(initial={'product_quantity': 1, 'product_id': product_id})  # Creats a form to add to cart

        user_messages = get_messages(request)
        return render(request, 'shop/product.html', {'form': form,
                                                     'product': instance,
                                                     'images': images,
                                                     'tags': tags,
                                                     'finalPrice': finalPrice,
                                                     'relatedProducts': relatedProducts,
                                                     'user_message': user_messages})


def add_to_basket(request):
    """Adds a selected product to the shopping cart. Cart items in cookie are stored as prod_id: quantity"""
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
            # messages.add_message(request, level, message, extra_tags='', fail_silently=False)
            messages.add_message(request, messages.INFO, "Product added to cart!")
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
