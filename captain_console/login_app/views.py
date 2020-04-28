from django.shortcuts import render

# Create your views here.


# login page view ( /login )
def login(request):
    return render(request, "login/login.html")
