from django.db import models
from shop.models import Product

NO_IMAGE = 'static/images/no-image-found.png'  # constant for missing images


# Create your models here.
class BannerImages(models.Model):
    imageURL = models.CharField(max_length=999, default=NO_IMAGE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
