from django.urls import path
from .views import AdminSessionView, UserSessionView

urlpatterns = [
    path('admin-session/', AdminSessionView.as_view(), name='admin-session'),
    path('user-session/', UserSessionView.as_view(), name='user-session'),
]