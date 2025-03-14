from django.db import models
from core.utils import generate_unique_id
from authentication.models import User
from orders.models import ShoppingCart  # Forward reference, defined later

class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_id("PRD"))
    name = models.CharField(max_length=100)
    description = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_products')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_products')
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id("PRD", Product)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Product'

class PriceBook(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_id("PRC"))
    productId = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_books')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_price_books')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_price_books')
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id("PRC", PriceBook)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.productId.name} - ${self.price}"

    class Meta:
        db_table = 'PriceBook'

class ProductItem(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_id("ITM"))
    productId = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    shoppingCartId = models.ForeignKey('orders.ShoppingCart', on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_product_items')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_product_items')
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id("ITM", ProductItem)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.productId.name} (x{self.quantity}) in Cart {self.shoppingCartId.id}"

    class Meta:
        db_table = 'ProductItem'