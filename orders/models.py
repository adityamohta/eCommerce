from django.conf import settings
from django.db import models


class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)   # not required.
    email = models.EmailField(unique=True)    # required.

    def __str__(self):
        return self.email


ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=120)

    def __str__(self):
        return "%s | %s, %s, %s - %s | %s" % (self.type, self.street, self.city, self.state, self.zipcode, self.user)


# class Order(models.model):
#     # cart
#     # user_checkout --> required.
#     # shipping address
#     # billing address
#     # shipping total
#     # order total (cart total + shipping)
#     # order_id --> custom_id
