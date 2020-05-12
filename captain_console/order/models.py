from django.db import models
from user.models import User


# Create your models here.


class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status


class Order(models.Model):
    order_id = models.CharField(max_length=15, default="")
    items = models.CharField(max_length=300, default="")
    date = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(OrderStatus, blank=True, null=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(default="email@email.com")
    full_name = models.CharField(max_length=70, blank=True, default="")
    address = models.CharField(max_length=32, blank=True, default="")
    country = models.CharField(max_length=32, blank=True, default="")
    city = models.CharField(max_length=32, blank=True, default="")
    postal_code = models.CharField(max_length=12, blank=True, default="")
    note = models.CharField(max_length=100, blank=True, default="")

    def get_order_data(self):
        return self.order_items.get_products()

    def get_total_price(self):
        return self.order_items.get_total_price()

    def null_cart(self):
        self.order_items.empty_cart()
        return

    def __str__(self):
        return self.order_id

