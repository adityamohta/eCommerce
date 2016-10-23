from django.contrib import admin

from .models import UserCheckout, UserAddress


class UserAddressModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'city', 'zipcode']

    class Meta:
        model = UserAddress


admin.site.register(UserCheckout)
admin.site.register(UserAddress, UserAddressModelAdmin)
