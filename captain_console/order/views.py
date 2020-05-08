from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from user.models import Address, User
from shop.models import Product, ProductImage
from cart.views import render_dict_cookie
from .forms import ShippingAddressForm, PaymentInfoForm, ShippingAddressInfoForm

# Create your views here.

def shipping(request):
    context = {}
    my_form = ShippingAddressInfoForm()
    if request.method == "POST":
        my_form = ShippingAddressInfoForm(request.POST)
        if my_form.is_valid():
            request.session['address'] = my_form.cleaned_data['address']
            request.session['country'] = my_form.cleaned_data['country']
            request.session['city'] = my_form.cleaned_data['city']
            request.session['postal_code'] = my_form.cleaned_data['postal_code']
            request.session['note'] = my_form.cleaned_data['note']
            return redirect('../payment/')
        else:
            my_form = ShippingAddressInfoForm()
    context = {'form': my_form}
    return render(request, 'order/shippingInfo.html', context)


def billing(request):
    my_form = PaymentInfoForm()
    if request.method == "POST":
        my_form = PaymentInfoForm(request.POST)
        if my_form.is_valid():
            my_form = my_form.cleaned_data
            cardholder_name = my_form['cardholder_name']
            credit_card_num = my_form['credit_card_num']
            expiry_date = my_form['expiry_date']
            CVC = my_form['CVC']
            return redirect(
                '../summary/?cardholder_name=' + cardholder_name
                + '&credit_card_num=' + credit_card_num + '&expiry_date=' + expiry_date + '&CVC=' + CVC)
        else:
            my_form = PaymentInfoForm()
    context = {'form': my_form}
    return render(request, 'order/paymentInfo.html', context)

def summary(request):
    print('KingKongBitch')
    print(request.session['address'])
    #TODO addContext
    # Initializing form list, since we are rendering multiple forms
    cart_cookie = request.COOKIES['cart']
    cart_dict = render_dict_cookie(cart_cookie)
    cart_keys = list(cart_dict.keys())
    productObjList = []

    # Sending a cart total value with the return context (call by name in template)
    cart_total = 0

    # Iterating over all the keys in the cart dictionary
    for product_id in cart_keys:
        quantity = int(cart_dict[str(product_id)])
        # Trying to fetch a product with the product id present in the cookie dict
        try:
            # Setting all return data values
            product = Product.objects.get(id=product_id)
            productObjList.append(product)
            product_image = ProductImage.objects.filter(product=product.id).first()
            cart_total += product.price * quantity

        # If the product we tried to fetch didn't exist we skip it and delete the key
        except Product.DoesNotExist:
            del cart_dict[product_id]
            continue

    return render(request, 'order/summaryPage.html', context={'cart_total': cart_total, 'productList': productObjList})


def success(request):
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
