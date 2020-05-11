from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from backend.forms.product_form import productCreateForm, productUpdateForm, categoryCreateForm
from shop.models import ProductImage
from shop.models import Product, Category, Tag
from user.models import Address, User

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
            product_image = ProductImage(image=request.POST['image'], product=product)
            product_image.save() #Creates product image instance in DB
            # Saves all product images if user decides to add more than one
            if form.data['image2']:
                product_image2 = ProductImage(image=request.POST['image2'], product=product)
                product_image2.save() # Creates product image instance in DB
            if form.data['image3']:
                product_image3 = ProductImage(image=request.POST['image3'], product=product)
                product_image3.save()
            if form.data['image4']:
                product_image4 = ProductImage(image=request.POST['image4'], product=product)
                product_image4.save()
            if form.data['image5']:
                product_image5 = ProductImage(image=request.POST['image5'], product=product)
                product_image5.save()
            # Saves tags if user decides to add some
            if form.data['tag']:
                tag = Tag(tag=request.POST['tag'], product=product)
                tag.save() # Creates tag instance in DB
            if form.data['tag2']:
                tag2 = Tag(tag=request.POST['tag2'], product=product)
                tag2.save()
            if form.data['tag3']:
                tag3 = Tag(tag=request.POST['tag3'], product=product)
                tag3.save()
            if form.data['tag4']:
                tag4 = Tag(tag=request.POST['tag4'], product=product)
                tag4.save()
            if form.data['tag5']:
                tag5 = Tag(tag=request.POST['tag5'], product=product)
                tag5.save()

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
            product_image = ProductImage(image=request.POST['image'], product=instance)
            product_image.save() # Creates product image instance in DB
            if form.data['image2']:
                product_image2 = ProductImage(image=request.POST['image2'], product=instance)
                product_image2.save()
            if form.data['image3']:
                product_image3 = ProductImage(image=request.POST['image3'], product=instance)
                product_image3.save()
            if form.data['image4']:
                product_image4 = ProductImage(image=request.POST['image4'], product=instance)
                product_image4.save()
            if form.data['image5']:
                product_image5 = ProductImage(image=request.POST['image5'], product=instance)
                product_image5.save()
            # Saves tags if user decides to add some
            if form.data['tag']:
                tag = Tag(tag=request.POST['tag'], product=instance)
                tag.save() # Creates product image instance in DB
            if form.data['tag2']:
                tag2 = Tag(tag=request.POST['tag2'], product=instance)
                tag2.save()
            if form.data['tag3']:
                tag3 = Tag(tag=request.POST['tag3'], product=instance)
                tag3.save()
            if form.data['tag4']:
                tag4 = Tag(tag=request.POST['tag4'], product=instance)
                tag4.save()
            if form.data['tag5']:
                tag5 = Tag(tag=request.POST['tag5'], product=instance)
                tag5.save()
            return redirect('backend_index')
    else:
        form = productUpdateForm(instance=instance)
    return render(request, 'backend/updateProduct.html', {'form': form, 'id': id})

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('backend_index')

def create_category(request):
    form = categoryCreateForm()
    if request.method == 'POST':
        form = categoryCreateForm(data=request.POST) # Creates the form
        if form.is_valid():
            form.save()
            return redirect('backend_index')
    else:
        form = categoryCreateForm()
    return render(request, 'backend/backendAddCategory.html', {'form': form})


def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect('backend_index')

#User views here

def backend_users(request):
    if request.method == "GET":
        return render(request, 'backend/backendUsers.html', context={"users": User.objects.all()})


#TODO def create_user(request):

"""def update_user(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = userUpdateForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('backend_product', id=id)
    else:
        form = productUpdateForm(instance=instance)
    return render(request, 'backend/updateProduct.html', {'form': form, 'id':id})"""




