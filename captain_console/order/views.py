from django.shortcuts import render, get_object_or_404, redirect
from user.models import Address, User
from shop.models import Product, ProductImage
from cart.views import render_dict_cookie
from .forms import ShippingAddressForm, PaymentInfoForm, ShippingAddressInfoForm, CartItemDisplay
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.
from .models import Order, OrderStatus


def shipping(request):
    # TODO add option to use saved address info for registered user
    # TODO If user is logged and has already entered address info but doesn't have it saved in profile, offer to save it for them
    my_form = ShippingAddressInfoForm()
    if request.method == "POST":
        my_form = ShippingAddressInfoForm(request.POST)
        if my_form.is_valid():  # Save address info into session
            request.session['full_name'] = my_form.cleaned_data['full_name']
            request.session['address'] = my_form.cleaned_data['address']
            request.session['country'] = my_form.cleaned_data['country']
            request.session['city'] = my_form.cleaned_data['city']
            request.session['postal_code'] = my_form.cleaned_data['postal_code']
            request.session['note'] = my_form.cleaned_data['note']

            if 'savePaymentInfoBox' in request.POST: # Saves user info if he checks the box
                user_id = request.user.id  # Users id from django auth
                user = User.objects.get(id=user_id)  # User instance
                address_id = user.address.id
                Address.objects.filter(id=address_id).update(full_name=my_form.cleaned_data['full_name'],
                                                            address=my_form.cleaned_data['address'],
                                                            country=my_form.cleaned_data['country'],
                                                            city=my_form.cleaned_data['city'],
                                                            postal_code=my_form.cleaned_data['postal_code'],
                                                            note=my_form.cleaned_data['note'])

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

    my_form = ShippingAddressInfoForm({'full_name': address.full_name, 'address': address.address,
                                       'country': address.country, 'city': address.city,
                                       'postal_code': address.postal_code, 'note': address.note})
    if request.method == "POST":
        my_form = ShippingAddressInfoForm({'full_name': address.full_name, 'address': address.address,
                                           'country': address.country, 'city': address.city,
                                           'postal_code': address.postal_code, 'note': address.note}, data=request.POST)
        # Save info in session
        request.session['full_name'] = my_form.cleaned_data['full_name']
        request.session['address'] = my_form.cleaned_data['address']
        request.session['country'] = my_form.cleaned_data['country']
        request.session['city'] = my_form.cleaned_data['city']
        request.session['postal_code'] = my_form.cleaned_data['postal_code']
        request.session['note'] = my_form.cleaned_data['note']
    else:
        context['form'] = my_form

    context['form'] = my_form
    return render(request, 'order/shippingInfo.html', context)


def billing(request):
    # TODO get form to acutally show validation errors

    my_form = PaymentInfoForm()
    if request.method == "POST":
        my_form = PaymentInfoForm(request.POST)
        if my_form.is_valid():

            my_form = my_form.cleaned_data  # TEMP SOLUTION: Save payment info into session
            # TODO possibly create payment info instance and store id in cookie

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
    if request.method == "GET":
        user=None
        cart_cookie = request.COOKIES['cart']
        # order_email = request.session['order_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            user = User.objects.get(id=user_id)

        order_status = OrderStatus.objects.get(id=1)
        order = Order(status=order_status, items=cart_cookie)  # Statuses: In progress, In shipping, Delivered
        order.save()

        primary_id = order.id
        secondary_id = "#CPTCS" + str(primary_id)
        order.order_id = secondary_id
        # order.email = order_email
        if user:
            order.user = user
        order.save()

        dict_cookie = render_dict_cookie(cart_cookie)
        product_keys = list(dict_cookie.keys())
        product_list = []
        total_price = 0
        for key in product_keys:
            product = Product.objects.get(id=int(key))
            quantity = int(dict_cookie[key])
            total_price += product.price*quantity
            data = {
                'quantity': quantity,
                'name': product.name,
                'price': product.price,
                'total': product.price*quantity
            }
            product_list.append(data)

        msg_plain = render_to_string('order/email.txt',
                                     context={'user': user, 'cart': product_list,
                                                'id': secondary_id, 'total_price': total_price, 'status': order.status})

        send_mail(
            'Order Confirmation from Captain Console '+secondary_id,
            msg_plain,
            'captainconsole69@gmail.com',
            ['agir96@gmail.com'],
        )
        # html_message=msg_html,

        response = render(request, 'order/confirmationPage.html', context={'order': order})
        response.set_cookie('cart', "")
        response.set_cookie('itm_count', 0)
        return response

    # @login_required() - TODO For using when user wants to use stored address


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
