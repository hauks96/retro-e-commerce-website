from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
from backend.forms.product_form import productCreateForm, productUpdateForm, categoryCreateForm, categoryDeleteForm
from backend.forms.user_forms import userCreateForm, userUpdateForm
from shop.models import ProductImage
from shop.models import Product, Category, Tag
from user.models import Address, User

# Create your views here.

# Create your views here.

#Product views

@staff_member_required()
def backend(request):
    if request.method == "GET":
        # if logged in fetch users cart
        # else load session data
        return render(request, 'backend/backendProducts.html', context={"products": Product.objects.all()})


@staff_member_required()
def backend_product(request, id):
    if request.method == "GET":
        return render(request, 'backend/backendSingleProduct.html', {'product': get_object_or_404(Product, pk=id)})


@staff_member_required()
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


@staff_member_required()
def update_product(request, id):
    product = get_object_or_404(Product, pk=id)
    productImages = ProductImage.objects.filter(product_id=id)
    tags = Tag.objects.filter(product_id=id)
    print(productImages)
    print(tags)
    if request.method == "POST":
        image = ProductImage.objects.filter(product_id=id).order_by("id", "-id").first()
        form = productUpdateForm(instance=product, initial={"image": "hello", "image2": "goodbye"}, data=request.POST)
        if form.is_valid():
            print(ProductImage.objects.filter(product_id=id).order_by("id", "-id").first())
            #form.cleaned_data['image'] = ProductImage.objects.filter(product_id=id).order_by("id", "-id").first()
            form.save()
            #product_image = ProductImage(image=request.POST['image'], product=instance)
            #product_image.save() # Creates product image instance in DB
            """if form.data['image2']:
                product_image2 = ProductImage(image=request.POST['image2'], product=product)
                product_image2.save()
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
                tag.save() # Creates product image instance in DB
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
                tag5.save()"""
            return redirect('backend_index')
    else:
        form = productUpdateForm(instance=product)
    return render(request, 'backend/updateProduct.html', {'form': form, 'id': id})


@staff_member_required()
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('backend_index')


@staff_member_required()
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


@staff_member_required()
def delete_category(request):
    form = categoryDeleteForm()
    if request.method == 'POST':
        form = categoryDeleteForm(data=request.POST)
        if form.is_valid():
            category_id = form.cleaned_data['category'].id
            category = get_object_or_404(Category, pk=category_id)
            category.delete()
            return redirect('backend_index')
    return render(request, 'backend/backendDeleteCategory.html', {'form': form})

#User views here


@staff_member_required()
def backend_users(request):
    if request.method == "GET":
        return render(request, 'backend/backendUsers.html', context={"users": User.objects.all()})


@staff_member_required()
def create_user(request):
    if request.method == 'POST':
        form = userCreateForm(data=request.POST) # Creates the form
        if form.is_valid():
            user = form.save(commit=False) # Creates the user
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            user.address = Address() # Creates an address instance for user
            # Saves all product images if user decides to add more than one

            return redirect('backend_users')
    else:
        form = userCreateForm()
    return render(request, 'backend/backendCreateUser.html', {'form': form})


@staff_member_required()
def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    return redirect('backend_users')


@staff_member_required()
def update_user(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = userUpdateForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('backend_users')
    else:
        form = userUpdateForm(instance=user)
    return render(request, 'backend/backendUpdateUser.html', {'form': form, 'id': id})





