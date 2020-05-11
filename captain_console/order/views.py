from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from user.models import Address, User
from shop.models import Product, ProductImage
from cart.views import render_dict_cookie
from .forms import ShippingAddressForm, PaymentInfoForm, ShippingAddressInfoForm, CartItemDisplay
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

def shipping(request):
    #TODO add option to use saved address info for registered user
    #TODO If user is logged and has already entered address info but doesn't have it saved in profile, offer to save it for them
    my_form = ShippingAddressInfoForm()
    if request.method == "POST":
        my_form = ShippingAddressInfoForm(request.POST)
        if my_form.is_valid(): # Save address info into session
            request.session['address'] = my_form.cleaned_data['address']
            request.session['country'] = my_form.cleaned_data['country']
            request.session['city'] = my_form.cleaned_data['city']
            request.session['postal_code'] = my_form.cleaned_data['postal_code']
            request.session['note'] = my_form.cleaned_data['note']
            if 'savePaymentInfoBox' in request.POST: # Saves user info if he checks the box
                user_id = request.user.id  # Users id from django auth
                user = User.objects.get(id=user_id)  # User instance
                address_id = user.address.id
                Address.objects.filter(id=address_id).update(address=my_form.cleaned_data['address'],
                                                            country= my_form.cleaned_data['country'],
                                                            city=my_form.cleaned_data['city'],
                                                            postal_code=my_form.cleaned_data['postal_code'],
                                                            note= my_form.cleaned_data['note'])
            return redirect('../payment/')
        else:
            return render(request, 'order/shippingInfo.html', {'form': my_form})
    return render(request, 'order/shippingInfo.html', {'form': my_form})


@login_required
def shipping_saved(request):
    context = {}
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    address = user.address
    my_form = ShippingAddressInfoForm({'address': address.address, 'country': address.country, 'city': address.city,
                                       'postal_code': address.postal_code, 'note': address.note})
    if request.method == "POST":
        my_form = ShippingAddressInfoForm({'address': address.address, 'country': address.country, 'city': address.city,
                                           'postal_code': address.postal_code, 'note': address.note}, data=request.POST)
        # Save info in session
        request.session['full_name'] = my_form.cleaned_data['full_name']
        request.session['address'] = my_form.cleaned_data['address']
        request.session['country'] = my_form.cleaned_data['country']
        request.session['city'] = my_form.cleaned_data['city']
        request.session['postal_code'] = my_form.cleaned_data['postal_code']
        request.session['note'] = my_form.cleaned_data['note']
        request.session['email'] = my_form.cleaned_data['email']
    else:
        context['form'] = my_form

    context['form'] = my_form
    return render(request, 'order/shippingInfo.html', context)



def billing(request):
    #TODO get form to acutally show validation errors
    my_form = PaymentInfoForm()
    if request.method == "POST":
        my_form = PaymentInfoForm(request.POST)
        if my_form.is_valid():
            my_form = my_form.cleaned_data # TEMP SOLUTION: Save payment info into session
            #TODO possibly create payment info instance and store id in cookie
            request.session["cardholder_name"] = my_form['cardholder_name']
            request.session["credit_card_num"] = my_form['credit_card_num']
            request.session["expiry_year"] = my_form['expiry_year']
            request.session["expiry_month"] = my_form['expiry_month']
            request.session["CVC"] = my_form['CVC']
            """return redirect(
                '../summary/?cardholder_name=' + cardholder_name
                + '&credit_card_num=' + credit_card_num + '&expiry_date=' + expiry_date + '&CVC=' + CVC)"""
            return redirect('../summary/')
        else:
            return render(request, 'order/paymentInfo.html', {'form': my_form})
    return render(request, 'order/paymentInfo.html', {'form': my_form})


def summary(request):
    cart_cookie = request.COOKIES['cart']
    cart_dict = render_dict_cookie(cart_cookie)
    cart_keys = list(cart_dict.keys())

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
            cart_total += product.price * quantity
            single_form = CartItemDisplay(initial={'quantity': quantity,
                                                'name': product.name,
                                                'price': product.price,
                                                'total_price': product.price * quantity,
                                                'image': product_image})
            # Appending all forms to the form list
            forms.append(single_form)

        # If the product we tried to fetch didn't exist we skip it and delete the key
        except Product.DoesNotExist:
            del cart_dict[product_id]
            continue

    return render(request, 'order/summaryPage.html', context={'cart_total': cart_total, 'forms': forms})


def success(request):
    cart_cookie = request.COOKIES['cart']
    cart_dict = render_dict_cookie(cart_cookie)
    cart_keys = list(cart_dict.keys())
    cart_total = 0
    productOrderList = []
    user = ""
    if request.user.is_authenticated():
        user_id = request.user.id
        user = User.objects.get(id=user_id)

    for product_id in cart_keys:
        quantity = int(cart_dict[str(product_id)])
        # Trying to fetch a product with the product id present in the cookie dict
        try:
            # Setting all return data values
            product = Product.objects.get(id=product_id)
            cart_total += product.price * quantity
            productOrderList.append((product, quantity)) #Adds tuple to product order list with product item and quantity, could change to form

        # If the product we tried to fetch didn't exist we skip it and delete the key
        except Product.DoesNotExist:
            del cart_dict[product_id]
            continue

    # TODO: create actual order instance
    # Order.objects.create(order_file=str(productOrderList), order_date = datetime.now(), order_status = "received", user = user)
    # TODO: empty cart_cookie
    # cart_cookie = request.COOKIES['cart']
    # request.delete_cookie('cart')

    return render(request, 'order/confirmationPage.html')

    #@login_required() - TODO For using when user wants to use stored address
"""context = {}
    user = get_object_or_404(User, pk=request.user.id)
    address = user.address
    form = ShippingAddressForm(instance=address)
    if request.method == "POST":
        form = ShippingAddressForm(instance=address, data=request.POST)
        if form.is_valid():
            form.save()
            #return redirect('billing-index') TODO redirect on to payment
    context['form'] = form
    return render(request, 'order/shippingInfo.html', context)"""
