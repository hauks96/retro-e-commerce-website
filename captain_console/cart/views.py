from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.views import render_dict_cookie, render_string_cookie
from shop.models import Product, ProductImage
from cart.froms import EditCartItem

# Create your views here.
# https://docs.djangoproject.com/en/3.0/topics/http/sessions/
# Fetch the cart screen


def cart(request):
    """Fetches all cart items and returns data to template"""
    if request.method == "GET":
        # try to fetch a cookie named 'cart'
        try:
            cart_cookie = request.COOKIES['cart']
        # if it fails to fetch, there is no cokkie, so we create a new empty cookie and return a response
        except KeyError:
            response = render(request, 'cart/cart.html')
            response.set_cookie('cart', "")
            return response

        # if the cart cookie exists but was empty, we return an empty cart page
        if cart_cookie == "":
            response = render(request, 'cart/cart.html')
            return response

        # The cart wasn't empty so we create a dictionary with the cookie data
        cart_dict = render_dict_cookie(cart_cookie)
        cart_keys = list(cart_dict.keys())

        # If there for some reason is no keys in the cart dictionary we created
        if not cart_keys:
            response = render(request, 'cart/cart.html')
            response.set_cookie('cart', "")
            return response
        # If there are keys in the cart dictionary we fetch the products
        else:
            # Initializing form list, since we are rendering multiple forms
            forms = []

            # Sending a cart total value with the return context (call by name in template)
            cart_total = 0

            # Iterating over all the keys in the cart dictionary
            for product_id in cart_keys:
                quantity = int(cart_dict[str(product_id)])
                # Trying to fetch a product with the product id present in the cookie dict
                try:
                    # Setting all return data values
                    product = Product.objects.get(id=product_id)
                    product_image = ProductImage.objects.filter(product=product.id).first()
                    cart_total += product.price*quantity
                    single_form = EditCartItem(initial={'quantity': quantity,
                                                        'product_id': int(product_id),
                                                        'name': product.name,
                                                        'price': product.price,
                                                        'total_price': product.price*quantity,
                                                        'image': product_image,
                                                        'remove': 'False',
                                                        'edit': 'False'})
                    # Appending all forms to the form list
                    forms.append(single_form)

                # If the product we tried to fetch didn't exist we skip it and delete the key
                except Product.DoesNotExist:
                    del cart_dict[product_id]
                    continue

            return render(request, 'cart/cart.html', context={'forms': forms, 'cart_total': cart_total})


def modify_cart(request):
    """Gets sent a single form from the cart page. After validation, form contains values: \n
    form.cleaned_data['product_id']:Integer -> The product's ID\n
    form.cleaned_data['name']:String -> The name of the product\n
    form.cleaned_data['price']:Float -> The unit price of a product\n
    form.cleaned_data['quantity']:Integer -> Represents the amount of the product\n
    form.cleaned_data['total_price']:Integer -> The total price of the item, given the quantity\n
    form.cleaned_data['edit']:String -> True/False string, giving away what is to be done in this method\n
    form.cleaned_data['remove']:String -> True/False string, giving away what is to be done in this method\n"""
    # Edit or delete cart item
    if request.method == "POST":
        form = EditCartItem(data=request.POST)
        if form.is_valid():
            true_false = {'True': True, 'False': False}
            is_edit = form.cleaned_data['edit']
            is_remove = form.cleaned_data['remove']

            # DEBUG return HttpResponse("<h1>" + str(is_remove) + "</h1>")
            quantity = int(form.cleaned_data['quantity'])
            product_id = str(form.cleaned_data['product_id'])

            cart_cookie = request.COOKIES['cart']
            cart_dict = render_dict_cookie(cart_cookie)

            if product_id not in cart_dict:
                return redirect('cart-index')

            if true_false[is_edit]:
                current_item_quantity = int(cart_dict[product_id])
                if quantity != current_item_quantity:
                    cart_dict[product_id] = int(quantity)

            elif true_false[is_remove]:
                del cart_dict[str(product_id)]

            cart_cookie = render_string_cookie(cart_dict)
            response = redirect('cart-index')
            response.set_cookie('cart', cart_cookie)
            return response

        return HttpResponse("<h1>"+str(form.errors)+"</h1>")