from django.db import models
from cart.models import Cart
from django import forms  # for password


# Create your models here.


class Address(models.Model):
    addr = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    postal_code = models.IntegerField()  # Maybe make CharField
    note = models.CharField(max_length=32)


class User(models.Model):
    username = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    image = models.CharField(max_length=999, default='Set a default image')
    enabled = models.BooleanField(default=True)

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
        return self.firstName + ' ' + self.lastName

    def get_cart(self):
        return self.cart.get_products()
