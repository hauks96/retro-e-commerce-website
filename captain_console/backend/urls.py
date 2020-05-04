from django.urls import path
from . import views

urlpatterns = [
    path('', views.backend, name='backend_index'),
    path('create_product/', views.create_product, name='create_product'),
]