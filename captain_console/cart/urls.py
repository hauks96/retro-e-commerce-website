from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart, name="cart-index"),
    path('edit_cart/', views.modify_cart, name="edit-cart-index")
]
