from rest_framework import serializers
from orders.models import ShoppingCart, Case
from authentication.models import User

class ShoppingCartSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ShoppingCart
        fields = ['id', 'userId', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById', 'isActive']
        read_only_fields = ['id', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById']

class CaseSerializer(serializers.ModelSerializer):
    accountId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Case
        fields = ['id', 'accountId', 'subject', 'description', 'status', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById', 'isActive']
        read_only_fields = ['id', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById']