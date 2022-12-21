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

    @transaction.atomic
    def disable(self):
        if self.active is False:
            return
        self.active = False
        self.save()
        self.articles.update(active=False)


class Article(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=10)
    stripe_price_id = models.CharField(max_length=1000, default="")
    stripe_product_id = models.CharField(max_length=1000,  default="")
    active = models.BooleanField(default=False)
    in_stock_quantity = models.IntegerField(default=0)
    out_stock_quantity = models.IntegerField(default=0)
    url = models.CharField(max_length=1000, default="")
    product = models.ForeignKey(
        'store.Product', on_delete=models.CASCADE, related_name='articles')

    def __repr__(self):
        return str(self)

    def get_price(self):
        return self.price

    def get_in_stock_quantity(self):
        return self.in_stock_quantity

    def validate_quantity(self, quantity, is_article_in_cart):
        if quantity is not None:

            if isinstance(quantity, int) and quantity >= 0:
                new_in_stock_quantity = self.in_stock_quantity - quantity

                if quantity == 0:

                    if is_article_in_cart:
                        return { "is_valid": True, "message": "Article removed from cart", "quantity": quantity, "new_in_stock_quantity": new_in_stock_quantity }
                    
                    else:
                        return { "is_valid": False, "message": "Cannot remove article if it's not in cart", "quantity": quantity, "new_in_stock_quantity": new_in_stock_quantity }

                elif new_in_stock_quantity >= 0:
                    return { "is_valid": True, "message": f"You have now {quantity} {self.name} in your cart", "quantity": quantity, "new_in_stock_quantity": new_in_stock_quantity }

                else:
                    return { "is_valid": False, "message": f"Not enough articles in stock. Only {self.in_stock_quantity} {self.name} remaining in stock", "quantity": quantity, "new_in_stock_quantity": new_in_stock_quantity  }

            else:
                return { "is_valid": False, "message": "Quantity need to be a integer greater than or equal to 0", "quantity": quantity, "new_in_stock_quantity": quantity  }

        else:
            return { "is_valid": False, "message": "Quantity cannot be blank", "quantity": quantity, "new_in_stock_quantity": quantity  }



class Cart(models.Model):

    user = models.ForeignKey('authentication.User',
                             on_delete=models.CASCADE, related_name="carts")

    def __repr__(self):
        return f'Cart(id={self.id}, user={self.user})'

    def get_articles(self, cart_serializer, cart_article_serializer):
        cart = self
        cart_articles = CartArticle.objects.filter(cart=cart)
        cart_serializer = cart_serializer(cart)
        cart_articles_serializer = cart_article_serializer(cart_articles, many=True)
        serialized_cart = cart_serializer.data
        serialized_cart_articles = cart_articles_serializer.data
        serialized_cart["cart_articles"] = serialized_cart_articles

        return serialized_cart


class CartArticle(models.Model):
    article = models.ForeignKey(
        'store.Article', on_delete=models.CASCADE, related_name='cart_articles')

    cart = models.ForeignKey(
        'store.Cart', on_delete=models.CASCADE, related_name='cart_articles')

    quantity = models.IntegerField(default=1)

    def __repr__(self):
        return f'CartArticle(id={self.id}, article={self.article}, cart={self.cart}, quantity={self.quantity})'
