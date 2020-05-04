from django.urls import path
from . import views

urlpatterns = [
    path('', views.backend, name='backend_index'),
    path('<int:id>', views.backend_product, name='backend_product'),
    path('create_product/', views.create_product, name='create_product'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('update_product/<int:id>', views.update_product, name='update_product'),
]