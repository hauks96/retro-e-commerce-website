from django.db import models


# Create your models here.
class Order(models.Model):
    order_file = models.CharField(max_length=2500, default="", blank=True) #Change to Binary Field to store file??
    order_date = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=50, blank=True)
    # Add user_id foreign key

    def get_order_data(self):
        return self.order_items.get_products()

    def get_total_price(self):
        return self.order_items.get_total_price()

    def null_cart(self):
        self.order_items.empty_cart()
        return


