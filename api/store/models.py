from django.db import models, transaction


class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    url = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name

    @transaction.atomic
    def disable(self):
        if self.active is False:
            return
        self.active = False
        self.save()
        self.products.update(active=False)


class Product(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    url = models.CharField(max_length=1000, default="")
    category = models.ForeignKey(
        'store.Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stripe_price_id =  models.CharField(max_length=1000, default="")
    stripe_product_id = models.CharField(max_length=1000,  default="")
    active = models.BooleanField(default=False)
    in_stock_quantity = models.IntegerField(default=0)
    out_stock_quantity = models.IntegerField(default=0)
    url = models.CharField(max_length=1000, default="")
    product = models.ForeignKey(
        'store.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name

    def get_price(self):
        return self.price
