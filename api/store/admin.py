from django.contrib import admin
from store.models import Category, Product, Article


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'active', 'description')


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'active',  'in_stock_quantity', 'out_stock_quantity')


class ArticleAdmin(admin.ModelAdmin):

    list_display = ('name', 'product', 'category', 'price')

    @admin.display(description='Category')
    def category(self, obj):
        return obj.product.category


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Article, ArticleAdmin)