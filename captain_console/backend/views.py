from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from backend.forms.product_form import productCreateForm
from shop.models import ProductImage
from shop.models import Product
from shop.views import shop

# Create your views here.

def backend(request):
    if request.method == "GET":
        # if logged in fetch users cart
        # else load session data
        return render(request, 'backend/backend.html')

def create_product(request):
    if request.method == 'POST':
        form = productCreateForm(data=request.POST) # Creates the form
        if form.is_valid():
            product = form.save()
            product_image = ProductImage(image=request.POST['image'], product=product) #Creates product image instance in DB
            product_image.save()
            return redirect('shop-index') # Change redirect to backend product view not user
    else:
        form = productCreateForm()
    return render(request, 'backend/create_product.html', {'form': form})
