from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login-index"),
    path('register/', views.register, name="register-index"),
    path('logout/', views.logout, name="logout-index"),
    path('profile/', views.profile, name="profile-index"),

]