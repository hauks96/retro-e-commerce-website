from django.urls import path
from . import views


urlpatterns = [
    path('checkout/shipping/', views.shipping, name="shipping-index"),
    path('checkout/shipping/saved', views.shipping_saved, name="shipping-index-saved"),
    path('checkout/payment/', views.billing, name="billing-index"),
    path('checkout/summary/', views.summary, name="summary-index"),
    path('checkout/success/', views.success, name="success"),
]
