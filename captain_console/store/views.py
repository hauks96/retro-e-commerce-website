from django.shortcuts import render
from django.http import HttpResponse


# home page view (index)
def index(request):
    return render(request, "store/index.html")
