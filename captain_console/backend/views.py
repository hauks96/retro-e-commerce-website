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
    """Displays all the site products in the main backend"""
    if request.method == "GET":
        return render(request, 'backend/backend_products.html',
                      context={"products": Product.objects.all().order_by('id')})


@staff_member_required()
def backend_users(request):
    """Displays all the site users in the main backend"""
    if request.method == "GET":
        return render(request, 'backend/backend_users.html', context={"users": User.objects.all().order_by('id')})


@staff_member_required()
def update_user(request, id):
    """Updates the information of a single user"""
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = userUpdateForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('backend_users')
    else:
        form = userUpdateForm(instance=user)
    return render(request, 'backend/backend_update_user.html', {'form': form, 'id': id})


@staff_member_required()
def create_product(request):
    """Creates a single product for the website"""
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
    """Creates a single tag for products"""
    if request.method == 'POST':
        form = singleTag(data=request.POST)
        if form.is_valid():
            new_tag = form.save()
            product = get_object_or_404(Product, pk=id)
            product.tag.add(new_tag)
            return redirect(update_product, id=id)
    else:
        form = singleTag()  # Creates the form

    return render(request, 'backend/add_tag.html', {'form': form, 'productID': id})


@staff_member_required()
def useTag(request, id):
    """Attaches an existing tag to an existing product"""
    if request.method == 'POST':
        form = selectTagForm(data=request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, pk=id)
            tag = form.cleaned_data['tag']
            product.tag.add(tag)
            return redirect(update_product, id=id)
    else:
        form = selectTagForm()  # Creates the form

    return render(request, 'backend/select_tag.html', {'form': form, 'productID': id})


@staff_member_required()
def deleteTag(request, id, productID):
    """Removes an attached tag from a product"""
    product = get_object_or_404(Product, pk=productID)
    tag = get_object_or_404(Tag, pk=id)
    product.tag.remove(tag)
    return redirect(update_product, id=productID)


@staff_member_required()
def createImage(request, id):
    """Create an image istance in the database and adds it to an existing product"""
    if request.method == 'POST':
        form = singleImage(initial={'product': id}, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(update_product, id=id)
    else:
        form = singleImage(initial={'product': id})  # Creates the form

    return render(request, 'backend/add_image.html', {'form': form, 'productID': id})


@staff_member_required()
def deleteImage(request, id):
    """Removes an image from the database and an existing product"""
    image = get_object_or_404(ProductImage, pk=id)
    productID = image.product.id
    image.delete()
    if not ProductImage.objects.filter(product_id=productID).exists(): # disables the product if it has no images
        product = get_object_or_404(Product, pk=productID)
        product.enabled = False
        product.save()

    return redirect(update_product, id=productID)


@staff_member_required()
def update_product(request, id):
    """Updates the information, images and tags of a product"""
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

    return render(request, 'backend/update_product.html', {'productID': id,
                                                          'form': form,
                                                          'tagforms': tagforms,
                                                          'imageforms': imageforms})


@staff_member_required()
def delete_product(request, id):
    """Deletes an individual product from the database"""
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('backend_index')


@staff_member_required()
def create_category(request):
    """Creates a new catagory for products to belong to"""
    form = categoryCreateForm()
    if request.method == 'POST':
        form = categoryCreateForm(data=request.POST)  # Creates the form
        if form.is_valid():
            form.save()
            return redirect('backend_index')
    else:
        form = categoryCreateForm()
    return render(request, 'backend/backend_add_category.html', {'form': form})


@staff_member_required()
def delete_category(request):
    """Deletes an existing category"""
    form = categoryDeleteForm()
    if request.method == 'POST':
        form = categoryDeleteForm(data=request.POST)
        if form.is_valid():
            category_id = form.cleaned_data['category'].id
            category = get_object_or_404(Category, pk=category_id)
            category.delete()
            return redirect('backend_index')
    return render(request, 'backend/backend_delete_category.html', {'form': form})


# User views here


@staff_member_required()
def create_user(request):
    """Creates an new user for the website"""
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
    return render(request, 'backend/backend_create_user.html', {'form': form})


@staff_member_required()
def delete_user(request, id):
    """Deletes an existing user"""
    user = get_object_or_404(User, pk=id)
    user.delete()
    return redirect('backend_users')


@staff_member_required()
def update_user(request, id):
    """Updates the information of an existing user"""
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = userUpdateForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('backend_users')
    else:
        form = userUpdateForm(instance=user)
    return render(request, 'backend/backend_update_user.html', {'form': form, 'id': id})


@staff_member_required()
def carousel(request):
    """Manages the carousel images shown on the homepage"""
    if request.method == "GET":
        return render(request, 'backend/carousel.html', context={"images": BannerImages.objects.all()})


@staff_member_required()
def carousel_add(request):
    """Adds an image to the carousel that links to an individual product"""
    if request.method == 'POST':
        form = carouselImageForm(data=request.POST)  # Creates the form
        if form.is_valid():
            BannerImages = form.save()  # Saves the BannerImages instance to the DB
            return redirect('carousel')
    else:
        form = carouselImageForm()
    return render(request, 'backend/add_to_carousel.html', {'form': form})


@staff_member_required()
def carousel_delete(request, id):
    """Deletes an existing image from the home page carousel"""
    banner_image = get_object_or_404(BannerImages, pk=id)
    banner_image.delete()
    return redirect('carousel')
