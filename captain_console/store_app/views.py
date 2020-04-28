from django.shortcuts import render
from django.http import HttpResponse


# home page view (index)
def shop_main(request):
    return render(request, 'shop/xxx.html')


