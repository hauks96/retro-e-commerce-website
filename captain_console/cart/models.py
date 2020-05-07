#OBSOLETE FILE - TO BE REMOVED

from django.core.validators import MinValueValidator
from django.db import models
from shop.models import Product
from django.contrib.sessions.models import Session


# Create your models here.


# This models data is to be saved to the session when a user adds something to basket and isn' logged in


class Cart(models.Model):

    def empty_cart(self):
        cart_items = CartItem.objects.all(cart=self.id)
        for item in cart_items:
            item.delete()

    def remove_item(self, item_id):
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()

    def get_total_price(self):
        total_price = 0
        for item in self.cart_items:
            total_price += item.item_total_price()

    def get_products(self):
        product_list = []
        cart_items = CartItem.objects.filter(cart=self.id)
        for item, i in enumerate(iterable=cart_items, start=1):
            product_list.append({
                'List number': i,
                'Name': item.product.name,
                'Quantity': item.product_quantity,
                'Unit price': item.product.price,
                'Total item price': item.item_total_price(),
            })
        return product_list


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    product_quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)

    def item_total_price(self):
        unit_price = self.product.price
        return unit_price * self.product_quantity
