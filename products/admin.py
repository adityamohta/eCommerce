from django.contrib import admin

from products.models import Product, ProductImage, Variation, Category, ProductFeatured


class ProductFeaturedInLine(admin.TabularInline):
    model = ProductFeatured
    extra = 0


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 10


class VariationInLine(admin.TabularInline):
    model = Variation
    extra = 0
    max_num = 10


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price']
    # list_editable = []
    inlines = [
        VariationInLine,
        ProductImageInLine,
        ProductFeaturedInLine
    ]

    class Meta:
        model = Product

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductImage)
# admin.site.register(ProductFeatured)
# admin.site.register(Variation)
