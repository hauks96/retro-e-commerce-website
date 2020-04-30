from django.shortcuts import render

# Create your views here.


# https://docs.djangoproject.com/en/3.0/topics/http/sessions/
# Fetch the cart screen
def cart(request):
    if request.method == "GET":
        #load session data
        return render(request, 'cart/cart.html')

    # Edit cart
    elif request.method == "PUT":
    # edit something from session data (cart menu)
    # change values etc
        return render(request, 'cart/cart.html')# reload the cart screen with updated data

    #Remove something from cart
    elif request.method  == "DELETE":
        #delete from django session data
        return render(request, 'cart/cart.html')# reload the cart


    #Add the "add to cart" request to user session
    elif request.method == "POST":
        #do something with request.data
        return render(request, 'cart/cart.html')#Render the previous screen

