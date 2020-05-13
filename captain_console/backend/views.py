from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.admin.views.decorators import staff_member_required
from backend.forms.product_form import productCreateForm, productUpdateForm, categoryCreateForm, categoryDeleteForm, \
    singleTag, singleImage, selectTagForm
from backend.forms.user_forms import userCreateForm, userUpdateForm
from backend.forms.carousel_forms import carouselImageForm
from shop.models import ProductImage
from shop.models import Product, Category, Tag
from user.models import Address, User
from home.models import BannerImages


@staff_member_required()
def backend(request):
    if request.method == "GET":
        return render(request, 'backend/backendProducts.html',
                      context={"products": Product.objects.all().order_by('id')})


@staff_member_required()
def backend_product(request, id):
    if request.method == "GET":
        return render(request, 'backend/backendSingleProduct.html', {'product': get_object_or_404(Product, pk=id)})


@staff_member_required()
def backend_users(request):
    if request.method == "GET":
        return render(request, 'backend/backendUsers.html', context={"users": User.objects.all().order_by('id')})


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


@staff_member_required()
def create_product(request):
    if request.method == 'POST':
        form = productCreateForm(data=request.POST)  # Creates the form
        if form.is_valid():
            product = form.save()
            product_image = ProductImage(image=request.POST['image'], product=product)
            product_image.save()  # Creates product image instance in DB
            # Saves all product images if user decides to add more than one
            return redirect('backend_index')
    else:
        form = productCreateForm()
    return render(request, 'backend/create_product.html', {'form': form})


@staff_member_required()
def createTag(request, id):
    if request.method == 'POST':
        form = singleTag(data=request.POST)
        if form.is_valid():
            new_tag = form.save()
            product = get_object_or_404(Product, pk=id)
            product.tag.add(new_tag)
            return redirect(update_product, id=id)
    else:
        form = singleTag()  # Creates the form

    return render(request, 'backend/addTag.html', {'form': form, 'productID': id})


@staff_member_required()
def useTag(request, id):
    if request.method == 'POST':
        form = selectTagForm(data=request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, pk=id)
            tag = form.cleaned_data['tag']
            product.tag.add(tag)
            return redirect(update_product, id=id)
    else:
        form = selectTagForm()  # Creates the form

    return render(request, 'backend/selectTag.html', {'form': form, 'productID': id})


@staff_member_required()
def deleteTag(request, id, productID):
    product = get_object_or_404(Product, pk=productID)
    tag = get_object_or_404(Tag, pk=id)
    product.tag.remove(tag)
    return redirect(update_product, id=productID)


@staff_member_required()
def createImage(request, id):
    if request.method == 'POST':
        form = singleImage(initial={'product': id}, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(update_product, id=id)
    else:
        form = singleImage(initial={'product': id})  # Creates the form

    return render(request, 'backend/addImage.html', {'form': form, 'productID': id})


@staff_member_required()
def deleteImage(request, id):
    image = get_object_or_404(ProductImage, pk=id)
    productID = image.product.id
    image.delete()
    return redirect(update_product, id=productID)


@staff_member_required()
def update_product(request, id):
    product = get_object_or_404(Product, pk=id)  # Gets our product
    tags = Tag.objects.filter(product=id)  # Gets the tags for that product
    tagforms = []  # Initializes a list of tag forms
    for tag in tags:  # Creates the list
        singleForm = singleTag(instance=tag)
        tagforms.append(singleForm)
    images = ProductImage.objects.filter(product=id)  # Gets the images for that product
    imageforms = []  # Initializes a list of image forms
    for image in images:  # Creates the list
        singleForm = singleImage(instance=image)
        imageforms.append(singleForm)

    if request.method == "POST":
        form = productUpdateForm(data=request.POST, instance=product)
        if form.is_valid():
            form.save()  # Saves the updates product to the database
            return redirect(update_product, id=id)
    else:
        form = productUpdateForm(instance=product)

    return render(request, 'backend/updateProduct.html', {'productID': id,
                                                          'form': form,
                                                          'tagforms': tagforms,
                                                          'imageforms': imageforms})


@staff_member_required()
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('backend_index')


@staff_member_required()
def create_category(request):
    form = categoryCreateForm()
    if request.method == 'POST':
        form = categoryCreateForm(data=request.POST)  # Creates the form
        if form.is_valid():
            form.save()
            return redirect('backend_index/')
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


# User views here


@staff_member_required()
def create_user(request):
    if request.method == 'POST':
        form = userCreateForm(data=request.POST)  # Creates the form
        if form.is_valid():
            user = form.save(commit=False)  # Creates the user
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            user.address = Address()  # Creates an address instance for user
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


@staff_member_required()
def carousel(request):
    if request.method == "GET":
        return render(request, 'backend/carousel.html', context={"images": BannerImages.objects.all()})


@staff_member_required()
def carousel_add(request):
    if request.method == 'POST':
        form = carouselImageForm(data=request.POST)  # Creates the form
        if form.is_valid():
            BannerImages = form.save()  # Saves the BannerImages instance to the DB
            return redirect('carousel')
    else:
        form = carouselImageForm()
    return render(request, 'backend/addToCarousel.html', {'form': form})


@staff_member_required()
def carousel_delete(request, id):
    banner_image = get_object_or_404(BannerImages, pk=id)
    banner_image.delete()
    return redirect('carousel')
