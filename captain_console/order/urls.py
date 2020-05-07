from django.urls import path
from . import views
"""path('shipping/', views.shipping, name="shipping-index"),
    path('billing/', views.billing, name="billing-index"),
    path('summary/', views.summary, name="summary-index"),
    path('<int:orderID>/confirmation', views.confirmation, name="confirmation-index")"""
urlpatterns = [
    path('checkout/shipping/', views.shipping, name="shipping-index"),
    path('checkout/payment/', views.shipping, name="shipping-index"),
    path('checkout/summary/', views.shipping, name="shipping-index"),
    path('checkout/success/', views.shipping, name="shipping-index"),
]
