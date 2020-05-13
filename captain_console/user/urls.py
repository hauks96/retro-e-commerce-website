from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    # Login/registration urls
    path('login/', LoginView.as_view(template_name='user/login.html'), name="login"),
    path('register/', views.register, name="register-index"),
    path('logout/', LogoutView.as_view(next_page='home-index'), name="logout"),

    # Profile urls
    path('profile/', views.profile, name="profile-index"),
    path('profile/edit_person/', views.user_edit, name='edit-person'),
    path('profile/edit_address/', views.address_edit, name='edit-address'),
    path('profile/edit_profile_pic/', views.change_profile_pic, name='edit-profile-pic'),

    # Search history urls
    path('profile/search_history/', views.search_history, name='search-history'),

    # Order urls
    path('profile/order_history/', views.order_history, name='order-history'),
    path('profile/order_history/<int:orderID>/', views.order_details, name='order-details'),
]