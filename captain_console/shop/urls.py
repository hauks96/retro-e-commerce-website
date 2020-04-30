from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name="shop-index"),
    path('<int:product_id>/', views.product, name="product-index"),
]