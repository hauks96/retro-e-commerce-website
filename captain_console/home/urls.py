from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home-index"),
    path('affiliate/', views.affiliate, name="affiliate"),
    path('shipping/', views.shipping, name='shipping'),
]