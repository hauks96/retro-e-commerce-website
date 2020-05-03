from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('login/', LoginView.as_view(template_name='user/login.html'), name="login"),
    path('register/', views.register, name="register-index"),
    path('logout/', LogoutView.as_view(next_page='home-index'), name="logout"),
    path('profile/', views.profile, name="profile-index"),

]