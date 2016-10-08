from django.contrib import admin

from products.models import Product, ProductImage, Variation, Category, ProductFeatured

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductFeatured)
admin.site.register(Variation)
