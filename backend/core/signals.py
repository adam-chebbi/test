from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps
from django_currentuser.middleware import get_current_user

@receiver(pre_save)
def set_audit_fields(sender, instance, **kwargs):
    """
    Auto-fill createdById and lastModifiedById based on the authenticated user.
    Applies to all models with audit fields.
    """
    # List of apps to apply this signal to
    applicable_apps = ['authentication', 'payments', 'products', 'orders', 'notifications', 'records']

    # Check if the sender's app is in the applicable list
    app_label = sender._meta.app_label
    if app_label not in applicable_apps:
        return

    # Check if the instance has audit fields
    has_audit_fields = all(hasattr(instance, field) for field in ['createdById', 'lastModifiedById', 'createdDate', 'lastModifiedDate'])
    if not has_audit_fields:
        return

    # Get the current user
    user = get_current_user()
    if user and not user.is_anonymous:
        if instance.pk is None:  # New instance
            if not instance.createdById:
                instance.createdById = user
        instance.lastModifiedById = user
    # Note: createdDate and lastModifiedDate are handled by auto_now_add and auto_now