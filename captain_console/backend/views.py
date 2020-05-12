from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.admin.views.decorators import staff_member_required
from backend.forms.product_form import productCreateForm, productUpdateForm, categoryCreateForm, categoryDeleteForm, singleTag
from backend.forms.user_forms import userCreateForm, userUpdateForm
from backend.forms.carousel_forms import carouselImageForm
from shop.models import ProductImage
from shop.models import Product, Category, Tag
from user.models import Address, User
from home.models import BannerImages



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
        form = productCreateForm(data=request.POST)  # Creates the form
        if form.is_valid():
            product = form.save()
            product_image = ProductImage(image=request.POST['image'], product=product)
            product_image.save()  # Creates product image instance in DB
            # Saves all product images if user decides to add more than one
            if form.data['image2']:
                product_image2 = ProductImage(image=request.POST['image2'], product=product)
                product_image2.save()  # Creates product image instance in DB
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
                tag.save()  # Creates tag instance in DB
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
def deleteTag(request, productID):
    print("hi")
    if request.method == "POST":
        pass
    return redirect(update_product(request, productID))

@staff_member_required()
def update_product(request, id):
    if request.method == "POST":
        # check if we're deleting a tag
        if "deleteTag" in request.POST:
            print("við komumst hingað inn en faum ekkert data.. held eg :)")
            print(request.POST['deleteTag'])
            print("delete tag")
            form = singleTag(request.POST)
            print(form)
        elif "updateInfo" in request.POST:
            print("updating info")
        instance = get_object_or_404(Product, pk=id)
        tags = Tag.objects.filter(product_id=id)  # delete me
        form = productUpdateForm(instance=instance)
        tagforms = []
        for tag in tags:
            singleForm = singleTag({'name': tag})
            tagforms.append(singleForm)
    else:
        instance = get_object_or_404(Product, pk=id)
        tags = Tag.objects.filter(product_id=id)  # delete me
        form = productUpdateForm(instance=instance)
        tagforms = []
        for tag in tags:
            singleForm = singleTag({'name': tag})
            tagforms.append(singleForm)

    return render(request, 'backend/updateProduct.html', {'id': id,
                                                          'form': form,
                                                          'tagforms': tagforms})



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


# User views here


@staff_member_required()
def backend_users(request):
    if request.method == "GET":
        return render(request, 'backend/backendUsers.html', context={"users": User.objects.all()})


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
        form = carouselImageForm(data=request.POST) # Creates the form
        if form.is_valid():
            BannerImages = form.save() # Saves the BannerImages instance to the DB
            return redirect('carousel')
    else:
        form = carouselImageForm()
    return render(request, 'backend/addToCarousel.html', {'form': form})


@staff_member_required()
def carousel_delete(request, id):
    banner_image = get_object_or_404(BannerImages, pk=id)
    banner_image.delete()
    return redirect('carousel')


