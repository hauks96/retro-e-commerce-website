from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegistrationForm, ProfileForm, AddressForm, ProfilePicForm
from django.contrib.auth import authenticate
from .models import User, Address, UserHistory
from order.models import Order

from order.forms import CartItemDisplay
from shop.models import Product, ProductImage
from shop.views import render_dict_cookie


# Create your views here.


# login page view ( user/login )


def login(request):
    user = authenticate(username=request.data["username"], password=request.data["password"])
    if user:
        #  user exists, redirect to home-index
        return render(request, "home/home.html")
    else:
        #  return an response and redirect to login-index
        return render(request, "user/login.html")


def register(request):
    context = {}
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            address = Address()
            address.save()
            user.address = address
            user.save()
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = UserRegistrationForm()
        context['registration_form'] = form
    return render(request, "user/register.html", context)


@login_required
def profile(request):
    user_id = request.user.id  # Users id from django auth
    user = User.objects.get(id=user_id)  # User instance
    address = user.address  # Users address instance

    return render(request, "user/profile.html", {
        'user': user,
        'address': address
    })


@login_required
def user_edit(request):
    context = {}
    user_id = request.user.id  # Users id from django auth
    user = User.objects.get(id=user_id)  # User instance
    form = ProfileForm(instance=user)
    if request.method == "POST":
        form = ProfileForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile-index')
        else:
            context['form'] = form

    context['form'] = form
    return render(request, 'user/edit_person.html', context)


@login_required
def address_edit(request):
    context = {}
    user_id = request.user.id  # Users id from django auth
    user = User.objects.get(id=user_id)  # User instance
    address = user.address
    form = AddressForm(instance=address)
    if request.method == "POST":
        form = AddressForm(instance=address, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile-index')
        else:
            context['form'] = form

    context['form'] = form
    return render(request, 'user/edit_address.html', context)


@login_required
def change_profile_pic(request):
    user_id = request.user.id  # Users id from django auth
    user = User.objects.get(id=user_id)  # User instance  # User instance
    form = ProfilePicForm(instance=user)
    # print(form)
    if request.method == "POST":
        form = ProfilePicForm(data=request.POST, instance=user)
        # print(form)
        if form.is_valid():
            # print(form.is_valid())
            form.save()
            return redirect('profile-index')
        else:
            form = ProfilePicForm(instance=user)

    return render(request, 'user/edit_profile_pic.html', {'form': form})


@login_required
def search_history(request):
    history = UserHistory.objects.filter(user=request.user.id).order_by('-date')
    context = {
        'history': history
    }
    return render(request, 'user/search_history.html', context)


@login_required
def order_history(request):
    if request.method == "GET":
        user = User.objects.get(id=request.user.id)
        orders = Order.objects.filter(user=user.id)

        return render(request, 'user/order_history.html', context={'orders': orders})


def order_details(request, orderID):
    if request.method == "GET":
        order = Order.objects.get(id=orderID)
        cart_cookie = order.items
        forms, cart_total = get_product_forms(cart_cookie)

        return render(request, 'user/order_details.html', context={'order': order, 'forms': forms, 'cart_total': cart_total})


def get_product_forms(cart_cookie):
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

    return forms, cart_total
