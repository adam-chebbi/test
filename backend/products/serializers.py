from rest_framework import serializers
from products.models import Product, PriceBook, ProductItem
from authentication.models import User
from orders.models import ShoppingCart

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById', 'isActive']
        read_only_fields = ['id', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById']

class PriceBookSerializer(serializers.ModelSerializer):
    productId = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = PriceBook
        fields = ['id', 'productId', 'price', 'discount', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById', 'isActive']
        read_only_fields = ['id', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById']

class ProductItemSerializer(serializers.ModelSerializer):
    productId = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    shoppingCartId = serializers.PrimaryKeyRelatedField(queryset=ShoppingCart.objects.all())

    class Meta:
        model = ProductItem
        fields = ['id', 'productId', 'shoppingCartId', 'quantity', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById', 'isActive']
        read_only_fields = ['id', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById']