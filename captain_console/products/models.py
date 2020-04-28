from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50) # Or whatever length we decide
    LongDescription = models.TextField(default="")
    price = models.DecimalField(decimal_places=2, max_digits=100)
    type = models.CharField(max_length=50)
    images = models.TextField() # How to best store images?