from django.db import models

NO_IMAGE = 'static/images/no-image-found.png'  # constant for missing images


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    image = models.CharField(max_length=999, default=NO_IMAGE)
    description = models.CharField(max_length=150, default="")

    def getName(self):
        return self.name

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    enabled = models.BooleanField(default=True, blank=True)
    discount = models.IntegerField(default=0, blank=True)
    short_description = models.CharField(max_length=150)
    long_description = models.CharField(max_length=999)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField(Tag)

    def get_category_name(self):
        return self.category.name

    def __str__(self):
        return self.name

    def getFinalPrice(self):  # returns a calculated price based on discount
        return self.price * (100 - self.discount) / 100

    def getProductImage(self):
        try:
            product_image = ProductImage.objects.filter(product_id=self.id).first()
        except:
            return 'https://www.saccon.it/img/coming-soon.jpg'

        return product_image.image


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.CharField(max_length=999)

    def __str__(self):
        return "Image for product: " + self.product.name

# can be called with Tags.objects.filter(product=product_id) to fetch all product tags
