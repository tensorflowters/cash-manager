from django.contrib import admin
from store.models import Category, Product, Article


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'active', 'description',
                    'url', 'date_created', 'date_updated')


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'description', 'active', 'category',
                    'url', 'date_created', 'date_updated')


class ArticleAdmin(admin.ModelAdmin):

    list_display = ('name', 'description', 'price', 'active', 'url',
                    'in_stock_quantity', 'out_stock_quantity', 'date_created', 'date_updated')

    @admin.display(description='Category')
    def category(self, obj):
        return obj.product.category


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Article, ArticleAdmin)
