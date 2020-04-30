from django.db import models
from shop.models import Product
from django.contrib.sessions.models import Session
# Create your models here.


# This models id is to be saved to the session when a user adds something to basket and isn' logged in
class CartItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    product_quantity = models.IntegerField(default=1)

    def item_total_price(self):
        unit_price = self.product.price
        return unit_price * self.product_quantity


class Cart(models.Model):
    cart_items = models.ManyToManyField(CartItem, blank=True)

    def empty_cart(self):
        self.cart_items.null()

    def get_total_price(self):
        total_price = 0
        for item in self.cart_items:
            total_price += item.item_total_price()

    def get_products(self):
        return_dict = {}
        for item, i in enumerate(iterable=self.cart_items.all(), start=1):
            return_dict[i] = {
                'Name': item.product.name,
                'Quantity': item.product_quantity,
                'Unit price': item.product.price,
                'Total item price': item.item_total_price(),
            }
        return return_dict








