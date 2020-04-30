from django.db import models
from shop.models import Product
from django.contrib.sessions.models import Session


# Create your models here.


# This models data is to be saved to the session when a user adds something to basket and isn' logged in
class CartItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    product_quantity = models.IntegerField(default=1)

    def item_total_price(self):
        unit_price = self.product.price
        return unit_price * self.product_quantity

    # if not logged in
    def update_session_data(self, session_cart: list, reorder=False) -> list:
        """This function takes in current session data, appends this objects data to the fetched data,
        and then returns the new data for the session. To update session set session[cart]=ret_data.
        To reorder session numeration in case of cart modifications use reorder=True"""
        if session_cart is None:
            session_cart = []

        if reorder:
            cart_data = []
            for item, i in enumerate(iterable=session_cart, start=1):
                cart_data.append({
                    'List number': i,
                    'Name': item.product.name,
                    'Quantity': item.product_quantity,
                    'Unit price': item.product.price,
                    'Total item price': item.item_total_price(),
                })
            session_cart = cart_data

        session_cart.append({
            'List number': len(session_cart)+1,
            'Name': self.product.name,
            'Quantity': self.product_quantity,
            'Unit price': self.product.price,
            'Total item price': self.item_total_price(),
        })
        return session_cart



class Cart(models.Model):
    cart_items = models.ManyToManyField(CartItem, blank=True)

    def empty_cart(self):
        self.cart_items.null()

    def get_total_price(self):
        total_price = 0
        for item in self.cart_items:
            total_price += item.item_total_price()

    def get_products(self):
        product_list = []
        for item, i in enumerate(iterable=self.cart_items.all(), start=1):
            product_list.append({
                'List number': i,
                'Name': item.product.name,
                'Quantity': item.product_quantity,
                'Unit price': item.product.price,
                'Total item price': item.item_total_price(),
            })
        return product_list
