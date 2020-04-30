from django.shortcuts import render


# Create your views here.
# https://docs.djangoproject.com/en/3.0/topics/http/sessions/
# Fetch the cart screen


def cart(request):
    if request.method == "GET":
        # if logged in fetch users cart
        # else load session data
        return render(request, 'cart/cart.html')


def modify_cart(request, product_id):
    # Edit cart
    if request.method == "PUT":
        # if logged in edit users cart
        # else edit something from session data
        return render(request, 'cart/cart.html')  # reload the cart screen with updated data

    # Remove something from cart
    elif request.method == "DELETE":
        # if logged in delete from users cart
        # else delete from session data
        return render(request, 'cart/cart.html')  # reload the cart

    # Add to cart
    elif request.method == "POST":
        # if logged in add to users cart
        # else add product + quantity to session data
        return render(request, 'cart/cart.html')  # Render the previous screen
