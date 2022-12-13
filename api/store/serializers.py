from rest_framework import serializers
from store.models import Category, Product, Article, Cart, CartArticle
from authentication.models import User


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'name', 'description', 'price',
                  'product', 'in_stock_quantity', 'url']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value

    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('Inactive product')
        return value


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'description',
                  'price', 'product', 'stripe_price_id', 'stripe_product_id', 'in_stock_quantity', 'out_stock_quantity', 'url']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value

    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('Inactive product')
        return value


class ProductSerializer(serializers.ModelSerializer):

    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'url', 'articles']


class ProductDetailSerializer(serializers.ModelSerializer):

    articles = ArticleDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated',
                  'name', 'description', 'active', 'category', 'url', 'articles']


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'url']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value


class CategoryDetailSerializer(serializers.ModelSerializer):

    products = ProductDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated',
                  'name', 'active', 'description', 'url', 'products']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value


class CartSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Cart
        fields = ['id', 'user']


class CartArticleSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    cart = serializers.SlugRelatedField(
        queryset=Cart.objects.all(), slug_field='id')
    article = ArticleSerializer(read_only=True)
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = CartArticle
        fields = ['id', 'cart', 'quantity', 'article']
