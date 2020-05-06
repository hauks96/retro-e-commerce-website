from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegistrationForm, ProfileForm, AddressForm, ProfilePicForm
from django.contrib.auth import authenticate
from .models import User, Address
from cart.models import Cart

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
            cart = Cart()
            cart.save()
            user.cart = cart
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


@login_required()
def address_edit(request):
    context = {}
    user_id = request.user.id  # Users id from django auth
    user = User.objects.get(id=user_id)  # User instance
    address = user.address
    form = AddressForm(instance=address)
    if request.method == "POST":
        form = AddressForm(instance=address, data=request.POST)
        if form.is_valid():
            #print(form.is_valid())
            form.save()
            return redirect('profile-index')
        else:
            context['form'] = form

    context['form'] = form
    return render(request, 'user/edit_address.html', context)

@login_required()
def change_profile_pic(request):
    user_id = request.user.id  # Users id from django auth
    user = User.objects.get(id=user_id)  # User instance  # User instance
    form = ProfilePicForm(instance=user)
    #print(form)
    if request.method == "POST":
        form = ProfilePicForm(data=request.POST, instance=user)
        #print(form)
        if form.is_valid():
            #print(form.is_valid())
            form.save()
            return redirect('profile-index')
        else:
            form = ProfilePicForm(instance=user)

    return render(request, 'user/edit_profile_pic.html', {'form': form})

@login_required()
def search_history():
    pass




