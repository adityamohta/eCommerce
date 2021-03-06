from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone

from products.models import Product, Variation, Category
from products.forms import VariationInventoryFormSet

from products.mixins import StaffRequiredMixin, LoginRequiredMixin
import random


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'products/product_list.html'


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        default_products = obj.default_category.all()
        products = (product_set | default_products).distinct()
        context['products'] = products
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'  # default value.

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        instance = self.get_object()
        # context['related'] = Product.objects.get_related(instance).order_by("?")[:6]
        context['related'] = sorted(Product.objects.get_related(instance)[:6], key=lambda x: random.random())

        return context


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()    # default value.
    template_name = 'products/product_list.html'  # default value.

    def get_context_data(self, *args, **kwargs):    # to add something to context variable.
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['now'] = timezone.now()
        context['query'] = self.request.GET.get('q', None)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs


class VariationListView(StaffRequiredMixin, ListView):
    model = Product
    queryset = Variation.objects.all()    # default value.
    template_name = 'products/variation_list.html'  # default value.

    def get_context_data(self, *args, **kwargs):    # to add something to context variable.
        context = super(VariationListView, self).get_context_data(*args, **kwargs)
        context['formset'] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get("pk")
        queryset = None
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)

        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                # if new_item.title:
                product_pk = self.kwargs.get('pk')
                product = get_object_or_404(Product, pk=product_pk)
                new_item.product = product
                new_item.save()

            html_message = '''
                <strong>Your inventory and pricing has been updated.</strong>
            '''
            html_message = settings.MESSAGE % ('success', html_message)
            messages.success(request, html_message, extra_tags='html_safe')

            return redirect("products:list")
        raise Http404

