from django.db import models
from core.utils import generate_unique_id
from authentication.models import User

class Notification(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_id("NTF"))
    message = models.TextField()
    image = models.BinaryField(null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    isRead = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_notifications')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_notifications')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_id("NTF", Notification)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notification {self.id} for {self.receiver.username}"

    class Meta:
        db_table = 'Notifications'