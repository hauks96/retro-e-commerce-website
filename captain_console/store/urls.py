from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Front Page!"),
    path('login', views.login)
]