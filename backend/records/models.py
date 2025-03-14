from django.db import models
from core.utils import generate_unique_id
from authentication.models import User

class RecordType(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_id("RTY"))
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_record_types')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_record_types')
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id("RTY", RecordType)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'RecordType'

class Address(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_id("ADR"))
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postalCode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_addresses')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_addresses')
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id("ADR", Address)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

    class Meta:
        db_table = 'Address'