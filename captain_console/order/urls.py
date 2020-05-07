from django.urls import path
from . import views


urlpatterns = [
    path('shippingInput/', views.shipping, name='shipping-index'),
    path('billing/', views.billing, name='billing-index'),
    path('summary/', views.summary, name='summary-index'),
    path('sumary/', views.summary, name='summary-index'), #temp path
    #path('<int:orderID>/confirmation', views.confirmation, name="confirmation-index"),

]
