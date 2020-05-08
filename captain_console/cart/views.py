from django.http import HttpResponse
from django.shortcuts import render, redirect
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
                                                        'remove': 'False',
                                                        'edit': 'False'})
                    forms.append(single_form)

                except Product.DoesNotExist:
                    continue

            return render(request, 'cart/cart.html', context={'forms': forms, 'cart_total': cart_total})


def modify_cart(request):
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