from rest_framework import serializers
from django.contrib.auth.models import User

from store.models import Category, Product, Article


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']



class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'active', 'description', 'url']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value


class CategoryDetailSerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name','active', 'description', 'products', 'url'] 

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductSerializer(queryset, many=True)
        return serializer.data


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'active', 'category', 'url']


class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'description', 'active', 'category', 'url']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'description', 'price', 'product', 'in_stock_quantity', 'out_stock_quantity', 'url']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value

    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('Inactive product')
        return value
