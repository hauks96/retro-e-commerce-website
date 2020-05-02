from django.shortcuts import render, redirect
from captain_console.forms.register_form import UserCreateForm
from django.contrib import messages

# Create your views here.


# login page view ( user/login )
def login(request):
    return render(request, "user/login.html")


def register(request):
    if request.method == "POST":
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login-index')
        else:
            print("not valid")
    else:
        form = UserCreateForm()
    return render(request, "user/register.html", {
        'form': form
    })


def profile(request):
    return


def logout(request):
    return
