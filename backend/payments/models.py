from django.db import models
from core.utils import generate_unique_id
from authentication.models import User
from django.contrib.auth.hashers import make_password

class BankCard(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_id("CRD"))
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_cards')
    cardNumber = models.CharField(max_length=255)  # Will store hashed value
    expiryDate = models.CharField(max_length=5)    # MM/YY, not hashed
    cvv = models.CharField(max_length=255)         # Will store hashed value
    cardHolderName = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_bank_cards')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_bank_cards')
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id("CRD", BankCard)
        # Hash sensitive fields on save
        if self.cardNumber and not self.cardNumber.startswith('$2b$'):  # Check if already hashed
            self.cardNumber = make_password(self.cardNumber)
        if self.cvv and not self.cvv.startswith('$2b$'):  # Check if already hashed
            self.cvv = make_password(self.cvv)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Card for {self.userId.username}"

    class Meta:
        db_table = 'BankCard'