from django.contrib import admin
from .models import Product, Category, ProductSize


class ProductSizeInline(admin.StackedInline):
    model = ProductSize
    extra = 0
    fields = ('size', 'quantity')
    raw_id_fields = ('size',)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    inlines = [ProductSizeInline, ]
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'display_size_and_type',
        'quantity',
    )

    def display_size_and_type(self, obj):
        return f"{obj.size.size} ({obj.size.size_type})"

    display_size_and_type.short_description = 'Size (Type)'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
