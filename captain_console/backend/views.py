from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from backend.forms.product_form import productCreateForm, productUpdateForm
from shop.models import ProductImage
from shop.models import Product

# Create your views here.

# Create your views here.

#Product views

def backend(request):
    if request.method == "GET":
        # if logged in fetch users cart
        # else load session data
        return render(request, 'backend/backendProducts.html', context={"products": Product.objects.all()})

def backend_product(request, id):
    if request.method == "GET":
        return render(request, 'backend/backendSingleProduct.html', {'product': get_object_or_404(Product, pk=id)})

def create_product(request):
    if request.method == 'POST':
        form = productCreateForm(data=request.POST) # Creates the form
        if form.is_valid():
            product = form.save()
            product_image = ProductImage(image=request.POST['image'], product=product) #Creates product image instance in DB
            product_image.save()
            return redirect('backend_index')
    else:
        form = productCreateForm()
    return render(request, 'backend/create_product.html', {'form': form})

def update_product(request, id):
    instance = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form = productUpdateForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('backendProduct', id=id)
    else:
        form = productUpdateForm(instance=instance)
    return render(request, 'backend/updateProduct.html', {'form': form, 'id':id})

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('backend_index')

#User views here


