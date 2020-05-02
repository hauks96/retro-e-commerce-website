from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# Create your views here.


# login page view ( user/login )


def login(request):
    return render(request, "user/login.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, "user/register.html", {
        'form': UserCreationForm()
    })


def profile(request):
    return


def logout(request):
    return
