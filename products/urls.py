from django.conf.urls import url

from products.views import ProductDetailView, ProductListView, VariationListView

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/inventory/$', VariationListView.as_view(), name='inventory'),
]
