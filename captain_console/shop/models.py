from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    enabled = models.BooleanField(default=True, blank=True)
    discount = models.IntegerField(default=0, blank=True)
    short_description = models.CharField(max_length=150)
    long_description = models.CharField(max_length=999)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_category_name(self):
        return self.category.name

    def __str__(self):
        return self.name


# can be called with ProductImages.objects.filter(product=product_id) to fetch all product images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.CharField(max_length=999)

    def __str__(self):
        return self.image


# can be called with Tags.objects.filter(product=product_id) to fetch all product tags
class Tag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50)
