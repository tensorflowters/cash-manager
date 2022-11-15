from rest_framework.serializers import ModelSerializer

from store.models import Category, Product, Article


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'active', 'description']


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'description', 'active', 'category']


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'description', 'price', 'product', 'in_stock_quantity', 'out_stock_quantity']