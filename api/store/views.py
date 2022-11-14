from rest_framework.viewsets import ReadOnlyModelViewSet

from store.models import Category, Product, Article 
from store.serializers import CategorySerializer, ProductSerializer, ArticleSerializer


class CategoryViewset(ReadOnlyModelViewSet):
 
    serializer_class = CategorySerializer
 
    def get_queryset(self):
        return Category.objects.all()


class ProductViewset(ReadOnlyModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class ArticleViewset(ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all()