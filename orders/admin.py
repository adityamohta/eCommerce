from django.contrib import admin

from .models import Order, UserCheckout, UserAddress


class UserAddressModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'city', 'zipcode']
    list_display_links = ['id', 'user']

    class Meta:
        model = UserAddress


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'billing_address', 'shipping_address', 'shipping_total_price', 'order_total', 'status']
    list_display_links = ['id', 'billing_address']

    class Meta:
        model = Order


class UserCheckoutModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'user']
    list_display_links = ['id', 'email']

    class Meta:
        model = UserCheckout


admin.site.register(Order, OrderModelAdmin)
admin.site.register(UserCheckout, UserCheckoutModelAdmin)
admin.site.register(UserAddress, UserAddressModelAdmin)
