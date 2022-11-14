from django.db import models


class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    in_stock_quantity = models.IntegerField(default=0)
    out_stock_quantity = models.IntegerField(default=0)

    category = models.ForeignKey('store.Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name