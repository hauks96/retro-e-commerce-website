from django.db import models
from user.models import User


# Create your models here.
class Order(models.Model):
    order_file = models.CharField(max_length=2500, default="", blank=True) #Change to Binary Field to store file??
    order_date = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def get_order_data(self):
        return self.order_items.get_products()

    def get_total_price(self):
        return self.order_items.get_total_price()

    def null_cart(self):
        self.order_items.empty_cart()
        return


