from django.db import models
from cart.models import Cart


# Create your models here.
class Order(models.Model):
    order_items = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)

    def get_order_data(self):
        return self.order_items.get_products()

    def get_total_price(self):
        return self.order_items.get_total_price()

    def null_cart(self):
        self.order_items.empty_cart()
        return
