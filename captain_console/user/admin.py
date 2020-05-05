# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

admin.site.register(User)
admin.site.register(Address)
