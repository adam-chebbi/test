from rest_framework import serializers
from records.models import RecordType, Address
from authentication.models import User

class RecordTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordType
        fields = ['id', 'name', 'description', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById', 'isActive']
        read_only_fields = ['id', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById']

class AddressSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Address
        fields = ['id', 'userId', 'street', 'city', 'state', 'postalCode', 'country', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById', 'isActive']
        read_only_fields = ['id', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById']