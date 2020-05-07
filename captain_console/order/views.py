from django.shortcuts import render, get_object_or_404, redirect
from user.models import Address, User
from .forms import ShippingAddressForm, PaymentInfoForm

# Create your views here.

def shipping(request):
    context = {}
    #user_id = request.user.id
    user = get_object_or_404(User, pk=request.user.id)
    address = user.address
    #address = get_object_or_404(Address, pk=address_id)
    print(request.method)
    form = ShippingAddressForm(instance=address)
    if request.method == "POST":
        form = ShippingAddressForm(instance=address, data=request.POST)
        if form.is_valid():
            form.save()
            #return redirect('billing-index') TODO redirect on to payment
    context['form'] = form
    return render(request, 'order/shippingInfo.html', context)


def billing(request): #TODO fix so that form renders in template
    context = {}
    form = PaymentInfoForm()
    print(request.method)
    if request.method == "POST":
        print(request.method)
        form = PaymentInfoForm(request.POST)
        if form.is_valid():
            print(form.is_valid())
            print(form.cleaned_data)
            context = {'form': form}
            #form.save()
            pass
    else:
        form = PaymentInfoForm()
        #print(form.errors)
    #context['form'] = form
    return render(request, 'order/paymentInfo.html', context)

def summary(request):
    #TODO addContext
    return render(request, 'order/summaryPage.html')


def success(request):
    return render(request, 'order/confirmationPage.html')
