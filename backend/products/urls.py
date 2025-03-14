from django.urls import path
from products.views import ProductListCreateView, ProductDetailView, PriceBookListCreateView, PriceBookDetailView, ProductItemListCreateView, ProductItemDetailView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<str:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('pricebooks/', PriceBookListCreateView.as_view(), name='pricebook-list-create'),
    path('pricebooks/<str:pricebook_id>/', PriceBookDetailView.as_view(), name='pricebook-detail'),
    path('productitems/', ProductItemListCreateView.as_view(), name='productitem-list-create'),
    path('productitems/<str:productitem_id>/', ProductItemDetailView.as_view(), name='productitem-detail'),
]