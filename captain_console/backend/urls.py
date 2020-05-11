from django.urls import path
from . import views

urlpatterns = [
    path('', views.backend, name='backend_index'),
    #products urls
    path('<int:id>/', views.backend_product, name='backend_product'),
    path('create_product/', views.create_product, name='create_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),
    path('create_category/', views.create_category, name='create_category'),
    #path('delete_category/', views.delete_category, name='delete_category'),
    #user urls
    path('users/', views.backend_users, name='backend_users'),
    #path('create_user', views.create_user, name='create_user')
]