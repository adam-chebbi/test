from rest_framework import serializers
from notifications.models import Notification
from authentication.models import User

class NotificationSerializer(serializers.ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    image = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Notification
        fields = ['id', 'message', 'image', 'receiver', 'isRead', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById']
        read_only_fields = ['id', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById', 'isRead']

    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        notification = Notification(**validated_data)
        if image_data:
            import base64
            notification.image = base64.b64decode(image_data)
        notification.save()
        return notification

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image', None)
        if image_data:
            import base64
            instance.image = base64.b64decode(image_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance