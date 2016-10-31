from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormMixin

from orders.forms import GuestCheckoutForm
from orders.models import UserCheckout, Order, UserAddress
from orders.mixins import CartOrderMixin
from products.models import Variation
from carts.models import Cart, CartItem


class ItemCountView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = request.session.get("cart_id")
            if request.user.is_authenticated():
                cart = Cart.objects.filter(user=request.user)
                if cart.count() >= 1:
                    cart = cart.first()
                    count = cart.cartitem_set.count()
                else:
                    count = 0
            elif cart_id is None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.cartitem_set.count()
            request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "carts/view.html"

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)
        cart_id = self.request.session.get("cart_id")
        if cart_id is not None:
            cart = Cart.objects.get(id=cart_id)
            if self.request.user.is_authenticated():
                cart.user = self.request.user
                cart.save()
            return cart

        if not self.request.user.is_authenticated():
            cart = Cart(subtotal=0.00)
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        else:
            cart = Cart.objects.filter(user=self.request.user)
            if cart.count() >= 1:
                cart = cart.first()
            else:
                cart = Cart(subtotal=0.00, user=self.request.user)
                cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
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
                line_total = cart_item.line_item_total
            except:
                line_total = None
            try:
                subtotal = cart_item.cart.subtotal
                tax_total = cart_item.cart.tax_total
                total = cart_item.cart.total
                # print(subtotal)
            except:
                subtotal = None
                tax_total = None
                total = None

            try:
                total_items = cart_item.cart.cartitem_set.count()
            except:
                total_items = 0

            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": line_total,
                "subtotal": subtotal,
                "flash_message": flash_message,
                "message_type": message_type,
                "total_items": total_items,
                "tax_total": tax_total,
                "total":  total
            }
            return JsonResponse(data)

        context = {
            "object": self.get_object(),
        }
        template = self.template_name

        return render(request, template, context)


class CheckoutView(CartOrderMixin, FormMixin, DetailView):
    model = Cart
    template_name = "carts/checkout_view.html"
    form_class = GuestCheckoutForm
    # success_url = "/checkout/"

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart is None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_check_id = self.request.session.get("user_checkout_id", None)

        if self.request.user.is_authenticated():
            user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
            user_checkout.user = self.request.user
            user_checkout.save()
            self.request.session["user_checkout_id"] = user_checkout.id
        elif not self.request.user.is_authenticated() and user_check_id is None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        else:
            pass

        if user_check_id is not None:
            user_can_continue = True

        context["order"] = self.get_order()
        context["user_can_continue"] = user_can_continue
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_checkout, created = UserCheckout.objects.get_or_create(email=email)
            request.session["user_checkout_id"] = user_checkout.id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout")

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)

        cart_id = self.request.session.get("cart_id")
        if cart_id is None:
            return redirect("cart")

        # cart = self.get_object()
        user_checkout_id = request.session.get("user_checkout_id")

        if user_checkout_id is not None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            new_order = self.get_order()

            if new_order.billing_address is None or new_order.shipping_address is None:
                return redirect("order_address")

            new_order.user = user_checkout
            new_order.save()

        return get_data


class CheckoutFinalView(CartOrderMixin, View):
    def post(self, request, *args, **kwargs):
        order = self.get_order()
        if order is None:
            return redirect("cart")
        if request.POST.get("payment_token") == "abcd":
            order.mark_completed()
            messages.success(request, "Thank you for your order. :)")
            del request.session["cart_id"]
            del request.session["order_id"]
        return redirect("order_detail", pk=order.pk)

    def get(self, request, *args, **kwargs):

        return redirect("checkout")
