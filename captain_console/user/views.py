from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages

# Create your views here.


# login page view ( user/login )
def login(request):
    return render(request, "user/login.html")


def register(request):
    context = {}
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login-index')
        else:
            context['registration_form'] = form
            print("not valid")
    else:
        form = UserRegistrationForm()
        context['registration_form'] = form
    return render(request, "user/register.html", context)


def profile(request):
    return


def logout(request):
    return
