from django.urls import path
from . import views


urlpatterns = [
    path('checkout/shipping/', views.shipping, name="shipping-index"),
    path('checkout/payment/', views.billing, name="billing-index"),
    path('checkout/summary/', views.summary, name="summary-index"),
    path('checkout/success/', views.success, name="success"),
]
