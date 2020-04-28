from django.shortcuts import render

# Create your views here.
# home page view (index)
def frontpage(request):
    return render(request, 'frontpage/frontpage.html')

