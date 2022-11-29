from rest_framework import serializers
from store.models import Category, Product, Article


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
                  'price', 'product', 'in_stock_quantity', 'out_stock_quantity', 'url']

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
