from django.contrib import admin

# Register your models here.
from shop.models import Product, ProductImage, Category, Tag

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Tag)