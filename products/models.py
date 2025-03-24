from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    categories = models.ManyToManyField('Category', related_name='products')
    #image =

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='categories')

    def __str__(self):
        return self.name