from django.contrib.auth.models import AbstractUser
from django.db import models
from cart.models import Cart
from django import forms  # for password


# Create your models here.


class Address(models.Model):
    addr = models.CharField(max_length=32, blank=True, default="")
    country = models.CharField(max_length=32, blank=True, default="")
    city = models.CharField(max_length=32, blank=True, default="")
    postal_code = models.CharField(max_length=12, blank=True, default="")  # Maybe make CharField
    note = models.CharField(max_length=32, blank=True, default="")


class User(AbstractUser):
    username = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=999, default="test123")
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=32, help_text="Enter first name")
    last_name = models.CharField(max_length=32, help_text="Enter last name")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    image = models.CharField(max_length=999, default='Set a default image')
    enabled = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    def validate_username(self):
        if len(self.username) > 12:
            return False
        usn = ''.join([i for i in self.username if not i.isdigit()])
        if not usn.isalpha():
            return False
        return True

    def get_address(self):
        return {
            'addr': self.address.addr,
            'country': self.address.country,
            'city': self.address.city,
            'postal_code': self.address.postal_code,
            'note': self.address.note
        }

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_cart(self):
        return self.cart.get_products()
