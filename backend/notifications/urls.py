from django.urls import path
from notifications.views import NotificationListCreateView, NotificationDetailView

urlpatterns = [
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<str:notification_id>/', NotificationDetailView.as_view(), name='notification-detail'),
]