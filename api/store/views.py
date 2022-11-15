from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from store.permissions import IsAdminAuthenticated, IsStaffAuthenticated
from store.models import Category, Product, Article
from store.serializers import CategoryDetailSerializer, CategoryListSerializer,\
    ProductDetailSerializer, ProductSerializer, ArticleSerializer


class MultipleSerializerMixin:

    detail_serializer_class = None

    @method_decorator(csrf_exempt)
    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    # permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]


class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        return Category.objects.filter(active=True)

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()


class ProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProductSerializer
    detail_serializer_class = ProductDetailSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()


class AdminProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ArticleViewset(ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset


class AdminArticleViewset(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()