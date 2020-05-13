from django.urls import path
from . import views

urlpatterns = [
    path('', views.backend, name='backend_index'),

    # products urls
    path('create_product/', views.create_product, name='create_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),

    # category urls
    path('create_category/', views.create_category, name='create_category'),
    path('delete_category/', views.delete_category, name='delete_category'),

    # carousel urls
    path('carousel/', views.carousel, name='carousel'),
    path('carousel_add/', views.carousel_add, name='carousel_add'),
    path('carousel_remove/<int:id>/', views.carousel_delete, name='carousel_remove'),

    # tag urls
    path('add_tag/<int:id>/', views.createTag, name='add_tag'),
    path('use_tag/<int:id>/', views.useTag, name='use_tag'),
    path('remove_tag/<int:id>/<int:productID>/', views.deleteTag, name='delete_tag'),

    # product image urls
    path('remove_image/<int:id>/', views.deleteImage, name='delete_image'),
    path('add_image/<int:id>/', views.createImage, name='add_image'),

    # user urls
    path('users/', views.backend_users, name='backend_users'),
    path('create_user', views.create_user, name='create_user'),
    path('delete_user<int:id>', views.delete_user, name='delete_user'),
    path('update_user<int:id>', views.update_user, name='update_user'),
]
