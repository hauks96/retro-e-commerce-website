from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, ProfileForm, AddressForm
from django.contrib.auth import authenticate
from .models import User

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


@login_required
def logout(request):
    return


def register(request):
    context = {}
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
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
            form.save()
            return redirect('profile-index')
        else:
            context['form'] = form

    context['form'] = form
    return render(request, 'user/edit_address.html', context)


@login_required()
def search_history():
    pass




