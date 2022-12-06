from rest_framework import serializers
from django.contrib.auth.models import User
from store.models import Category, Product, Article


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'email']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value

class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active', 'last_login', 'is_superuser']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value


class ArticleSerializer(serializers.ModelSerializer):

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
        fields = ['id', 'name', 'description',
                  'active', 'category', 'url', 'articles']


class ProductDetailSerializer(serializers.ModelSerializer):

    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated',
                  'name', 'description', 'active', 'category', 'url', 'articles']


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'active', 'description', 'url']

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
