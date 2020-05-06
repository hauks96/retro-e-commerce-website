from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name="shop-index"),
    path('<int:product_id>/', views.product, name="product-index"),
    path('<int:product_id>/add_to_basket/', views.add_to_basket, name='add-cart'),
]