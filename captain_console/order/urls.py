from django.urls import path
from . import views

urlpatterns = [
    path('shipping/', views.shipping, name="shipping-index"),
    path('billing/', views.billing, name="billing-index"),
    path('summary/', views.summary, name="summary-index"),
    path('<int:orderID>/confirmation', views.confirmation, name="confirmation-index"),
]
