from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
# https://docs.djangoproject.com/en/3.0/topics/http/sessions/
# Fetch the cart screen
from cart.models import CartItem
from shop.views import render_dict_cookie, render_string_cookie
from user.models import User
from shop.models import Product, ProductImage
from cart.froms import EditCartItem


def cart(request):
    """Fetches all cart items and returns data to template"""
    if request.method == "GET":
        try:
            cart_cookie = request.COOKIES['cart']
        except KeyError:
            response = render(request, 'cart/cart.html')
            response.set_cookie('cart', "")
            return response

        if cart_cookie == "":
            response = render(request, 'cart/cart.html')
            return response

        cart_dict = render_dict_cookie(cart_cookie)
        cart_keys = list(cart_dict.keys())

        if not cart_keys:
            response = render(request, 'cart/cart.html')
            response.set_cookie('cart', "")
            return response

        else:
            forms = []
            cart_total = 0
            for product_id in cart_keys:
                quantity = int(cart_dict[str(product_id)])
                try:
                    product = Product.objects.get(id=product_id)
                    product_image = ProductImage.objects.filter(product=product.id).first()
                    cart_total += product.price*quantity
                    single_form = EditCartItem(initial={'quantity': quantity,
                                                        'product_id': int(product_id),
                                                        'name': product.name,
                                                        'price': product.price,
                                                        'total_price': product.price*quantity,
                                                        'image': product_image,
                                                        'is_remove': False,
                                                        'is_edit': False})
                    forms.append(single_form)

                except Product.DoesNotExist:
                    continue

            return render(request, 'cart/cart.html', context={'forms': forms, 'cart_total': cart_total})


def modify_cart(request):
    # Edit cart
    if request.method == "POST":
        return HttpResponse("<p>"+str(request)+"<p>")
        # if logged in edit users cart
        # else edit something from session data
        return render(request, 'cart/cart.html')  # reload the cart screen with updated data



def delete_cart_item(item_id, cart_cookie=None):
    """Method to delete an product from cart.
    If cart_cookie argument is passed in, method returns string for cookie response, otherwise returns none"""
    if cart_cookie:
        cart_dict = render_dict_cookie(cart_cookie)
        if str(item_id) in cart_dict:
            del cart_dict[str(item_id)]
            string_cookie = render_string_cookie(cart_dict)
            return string_cookie

    return


def edit_item_quantity(item_id: int, new_quantity: int, cart_cookie=None):
    """Method to edit quantity of a cart product.
    If cart_cookie argument is passed in, method returns string for cookie response, otherwise returns none"""
    if cart_cookie:
        cart_dict = render_dict_cookie(cart_cookie)
        if str(item_id) in cart_dict:
            cart_dict[str(item_id)] = new_quantity
            string_cookie = render_string_cookie(cart_dict)
            return string_cookie
    return
