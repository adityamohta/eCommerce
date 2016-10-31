from django.contrib import admin

from .models import Cart, CartItem


class CartItemInLine(admin.TabularInline):
    model = CartItem


class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['id', 'user']

    inlines = [
        CartItemInLine,
    ]

    class Meta:
        model = Cart

admin.site.register(Cart, CartModelAdmin)
