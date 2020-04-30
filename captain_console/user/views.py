from django.shortcuts import render

# Create your views here.


# login page view ( user/login )
def login(request):
    return render(request, "user/login.html")


def register(request):
    return render(request, "user/register.html")


def profile(request):
    return


def logout(request):
    return