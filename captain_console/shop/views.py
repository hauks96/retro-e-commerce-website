from django.shortcuts import render

# Create your views here.
products = [{"name": "Crash Bandicoot", "price": 59.99, "description": "Quarantine Game of the year"}, #too be deleted obviously
            {"name": "Rachet and Clank", "price": 29.99, "description": "Nostalgic overload"}]

def shop(request):
    if 'search_filter' in request:
        #filter by search filter
        pass
    elif 'product_type' in request:
        #filter by product type
        pass
    elif 'by_name' in request:
        #filter by name value asc/desc
        pass
    else:
        #return all data
        pass

    return render(request, 'shop/shop.html', context={"products": products})

def product(request, product_id):
    #fetch product data or return 404
    #if user.is_authenticated -> save search to search hisory model
    #load product details page
    return render(request, 'shop/product.html')
