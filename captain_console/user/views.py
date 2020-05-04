from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileForm
from django.contrib.auth import authenticate
from .models import Profile


# Create your views here.


# login page view ( user/login )


def login(request):
    #  Requires an ajax request
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
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = UserRegistrationForm()
        context['registration_form'] = form
    return render(request, "user/register.html", context)


def profile(request):
    profile = Profile.objects.filter(user=request.user).first()  # fetch user, change to .get() and add try except
    if request.method == "POST":
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile-index')
    return render(request, "user/profile.html", {
        'form': ProfileForm(instance=profile)
    })


def logout(request):
    return
