from django.db import models
from cart.models import Cart


# Create your models here.


class Address(models.Model):
    addr = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    postal_code = models.IntegerField()
    note = models.CharField(max_length=32)


class User(models.Model):
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    username = models.CharField(max_length=12)
    email = models.EmailField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    image = models.CharField(max_length=999, default='Set a default image')
    enabled = models.BooleanField(default=True)

    def validate_username(self):
        if len(self.username) > 6 or len(self.username) > 12:
            raise ValueError
        return

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

