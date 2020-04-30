from django.db import models

# Create your models here.
class Product(models.Model):
    #attributes
    #inherits category as foreign key - on delete model.cascade
    pass

class Categories(models.Model):
    #attributes
    pass

class ProductImages(models.Model):
    #attributes M-M
    #productID
    #image
    pass
