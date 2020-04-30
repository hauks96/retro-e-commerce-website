from django.shortcuts import render

# Create your views here.
# home page view (index)
def home(request):
    return render(request, 'home/home.html')

