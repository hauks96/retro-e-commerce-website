from django.shortcuts import render, redirect
from user.models import Address, User
from shop.models import Product
from cart.views import render_dict_cookie
from .forms import PaymentInfoForm, ShippingAddressInfoForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Order, OrderStatus
from user.views import get_product_forms


# Create your views here.


def shipping(request):
    """Takes in shipping information from the user, validates it and saves it to the current session. Also includes
    the option to save the entered shipping information to the account"""
    checkout_is_valid = check_cart_before_checkout(request) 
    if not checkout_is_valid:  # Checks if the user is allowed to enter shipping information
        return redirect('shop-index')
    request.session['shipping_process'] = 'True'
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
            request.session['address_email'] = my_form.cleaned_data['address_email']

            if 'savePaymentInfoBox' in request.POST:  # Saves user info if he checks the box
                user_id = request.user.id  # Users id from django auth
                user = User.objects.get(id=user_id)  # User instance
                address_id = user.address
                Address.objects.filter(id=address_id).update(full_name=my_form.cleaned_data['full_name'],  # Updating
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
    """The same basic functionality as the above shipping function except it requires a login and lets the user
    use the shipping information saved to their account"""
    checkout_is_valid = check_cart_before_checkout(request)
    if not checkout_is_valid: # Checks if the user is allowed to enter shipping information
        return redirect('shop-index')

    request.session['shipping_process'] = 'True'
    context = {}
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    address = user.address

    if request.method == "POST":
        my_form = ShippingAddressInfoForm(data=request.POST)
        # Save info in session
        request.session['full_name'] = my_form.cleaned_data['full_name']
        request.session['address'] = my_form.cleaned_data['address']
        request.session['country'] = my_form.cleaned_data['country']
        request.session['city'] = my_form.cleaned_data['city']
        request.session['postal_code'] = my_form.cleaned_data['postal_code']
        request.session['note'] = my_form.cleaned_data['note']
        request.session['address_email'] = my_form.cleaned_data['address_email']
    else:
        my_form = ShippingAddressInfoForm({'full_name': address.full_name, 'address': address.address,
                                           'country': address.country, 'city': address.city,
                                           'postal_code': address.postal_code, 'note': address.note,
                                           'address_email': user.email})  # Initializes the form with the shipping info
        context['form'] = my_form

    context['form'] = my_form
    return render(request, 'order/shippingInfo.html', context)


def billing(request):
    """Takes in payment information from the user, validates it and saves it to the current session."""
    try:
        has_done_shipping = request.session['shipping_process']  # Checks if the user has completed the shipping information process of the checkout
    except KeyError:
        return redirect('shop-index')

    if has_done_shipping != "True":
        return redirect('cart-index')

    request.session['billing_process'] = 'True'

    my_form = PaymentInfoForm()
    if request.method == "POST":
        my_form = PaymentInfoForm(request.POST)
        if my_form.is_valid():
            my_form = my_form.cleaned_data
            request.session["cardholder_name"] = my_form['cardholder_name']
            request.session["credit_card_num"] = my_form['credit_card_num']
            request.session["expiry_year"] = my_form['expiry_year']
            request.session["expiry_month"] = my_form['expiry_month']
            request.session["CVC"] = my_form['CVC']
            return redirect('../summary/')
        else:
            return render(request, 'order/paymentInfo.html', {'form': my_form})
    return render(request, 'order/paymentInfo.html', {'form': my_form})


def summary(request):
    """Displays the summary of the user order"""
    try:
        has_done_billing = request.session['billing_process']  # Checks if the user has completed the payment information process of the checkout
    except KeyError:
        return redirect('shop-index')

    if has_done_billing != "True":
        return redirect('cart-index')

    request.session['summary_process'] = 'True'

    cart_cookie = request.COOKIES['cart']
    forms, cart_total = get_product_forms(cart_cookie)
    return render(request, 'order/summaryPage.html', context={'cart_total': cart_total, 'forms': forms})


def success(request):
    """Lets the user know that his order was succesful and sends the order information to the given email"""
    try:
        has_done_summary = request.session['summary_process']  # Checks if the user has been to the summary page of the order process
    except KeyError:
        return redirect('shop-index')

    if has_done_summary != "True":
        if request.user.is_authenticated:
            return redirect('order-history')
        return redirect('cart-index')


    if request.method == "GET":
        user = None
        cart_cookie = request.COOKIES['cart']

        if cart_cookie == "" or request.session['credit_card_num'] == "":
            if request.user.is_authenticated:
                return redirect('order-history')
            return redirect('home-index')

        if request.user.is_authenticated:
            user_id = request.user.id
            user = User.objects.get(id=user_id)

        order_status = OrderStatus.objects.get(id=1)
        order = Order(status=order_status, items=cart_cookie)  # Statuses: In progress, In shipping, Delivered
        order.save()

        primary_id = order.id
        secondary_id = "#CPTCS" + str(primary_id)
        order.order_id = secondary_id
        if user:
            order.user = user

        address_data = get_session_address(request)  # Sets the order information
        order.email = request.session['address_email']
        order.address = address_data['address']
        order.country = address_data['country']
        order.city = address_data['city']
        order.postal_code = address_data['postcode']
        order.full_name = address_data['full_name']
        order.note = address_data['note']
        order.save() #  Saves the order instance

        dict_cookie = render_dict_cookie(cart_cookie)  # Renders the shopping cart cookie into a dictionary
        product_keys = list(dict_cookie.keys())  # Creates a list of the product id in the shopping cart
        product_list = []
        total_price = 0
        for key in product_keys:  # For each product in the shopping cart
            product = Product.objects.get(id=int(key))  # Get the product instance
            quantity = int(dict_cookie[key])  # Set the quantity from the shopping cart
            final_price = float(product.price) * (1.0 - (float(product.discount) / 100.0))  # Calculates the discount
            total_price += final_price * float(quantity)  # Calculates the total price for that quantity of that product
            data = {  # Creates the information to be sent in the email
                'quantity': quantity,
                'name': product.name,
                'price': final_price,
                'total': final_price * float(quantity)
            }
            product_list.append(data)  # Adds the information to the product list

        msg_plain = render_to_string('order/email.txt',
                                     context={'user': user, 'cart': product_list,
                                              'id': secondary_id, 'total_price': total_price, 'status': order.status})

        send_mail(  # Sends the email
            'Order Confirmation from Captain Console ' + secondary_id,
            msg_plain,
            'captainconsole69@gmail.com',
            [order.email],
        )
        # html_message=msg_html,

        request.session['full_name'] = ""
        request.session['address'] = ""
        request.session['country'] = ""
        request.session['city'] = ""
        request.session['postal_code'] = ""
        request.session['note'] = ""
        request.session["cardholder_name"] = ""
        request.session["credit_card_num"] = ""
        request.session["expiry_year"] = ""
        request.session["expiry_month"] = ""
        request.session["CVC"] = ""
        request.session['billing_process'] = ""
        request.session['summary_process'] = ""
        request.session['shipping_process'] = ""
        response = render(request, 'order/confirmationPage.html', context={'order': order})
        response.set_cookie('cart', "")
        response.set_cookie('itm_count', 0)
        return response


def get_session_address(request):
    """Retrieves the address information from the session and renders it into a dictionary"""
    addr_dict = {'full_name': request.session['full_name'],
                 'address': request.session['address'],
                 'country': request.session['country'],
                 'city': request.session['city'],
                 'postcode': request.session['postal_code'],
                 'note': request.session['note']}
    return addr_dict


def check_cart_before_checkout(request):
    try:
        cart_cookie = request.COOKIES['cart']
    except KeyError:
        return False

    if cart_cookie == "":
        return False
    else:
        try:
            cart_dict = render_dict_cookie(cart_cookie)
        except IndexError:
            return False

    return True

