from django.db import models
from core.utils import generate_unique_id
from authentication.models import User

class ShoppingCart(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_id("CRT"))
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_carts')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_carts')
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id("CRT", ShoppingCart)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cart {self.id} for {self.userId.username}"

    class Meta:
        db_table = 'ShoppingCart'

class Case(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_id("CAS"))
    accountId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, default="New")
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_cases')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_cases')
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id("CAS", Case)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Case {self.id}: {self.subject}"

    class Meta:
        db_table = 'Case'