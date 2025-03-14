from rest_framework import serializers
from payments.models import BankCard
from authentication.models import User

class BankCardSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BankCard
        fields = ['id', 'userId', 'cardNumber', 'expiryDate', 'cvv', 'cardHolderName', 'isActive']
        read_only_fields = ['id']