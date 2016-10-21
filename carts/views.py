from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404, render

from products.models import Variation
from carts.models import Cart, CartItem


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "carts/view.html"

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)
        cart_id = self.request.session.get("cart_id")
        if cart_id is None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        flash_message = ""
        message_type = "info"
        item_added = False
        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            qty = 1
            try:
                qty = int(request.GET.get("qty"))
                if qty < 1:
                    delete_item = True
            except:
                raise Http404
            try:
                cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            except:
                cart_item = CartItem.objects.filter(cart=cart, item=item_instance)
                if cart_item.exists():
                    cart_item = cart_item.first()
                    created = False
                else:
                    cart_item = CartItem(cart=cart, item=item_instance)
                    created = True

            if created:
                flash_message = "Successfully added to the Cart"
                message_type = "success"
                item_added = True
            if delete_item:
                flash_message = "Item removed Successfully."
                cart_item.delete()
                message_type = "danger"
            else:
                if not created:
                    flash_message = "Quantity has been updated Successfully."
                    message_type = "info"
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))

        if request.is_ajax():
            try:
                total = cart_item.line_item_total
            except:
                total = None
            try:
                subtotal = cart_item.cart.subtotal
                # print(subtotal)
            except:
                subtotal = None

            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": total,
                "subtotal": subtotal,
                "flash_message": flash_message,
                "message_type": message_type,
            }
            return JsonResponse(data)

        context = {
            "object": self.get_object(),
        }
        template = self.template_name

        return render(request, template, context)
