from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from authentication.permissions import IsAdmin, IsUser
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from core.utils import api_response, paginate_queryset
import logging

logger = logging.getLogger('notifications')

class NotificationListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.profileName.name == "SUPER-ADMIN":
                notifications = Notification.objects.all()
            else:
                notifications = Notification.objects.filter(receiver=request.user)
            paginated_data = paginate_queryset(notifications, request)
            serializer = NotificationSerializer(paginated_data['results'], many=True)
            logger.info(f"Retrieved {paginated_data['count']} notifications for {request.user.username}")
            return api_response(
                data={"notifications": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
                message="Notifications retrieved successfully"
            )
        logger.warning("Unauthenticated user attempted to access notifications")
        return api_response(message="Authentication required", status_code=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if not request.user.is_authenticated or request.user.profileName.name not in ["SUPER-ADMIN", "ADMIN"]:
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to create notification")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()
            logger.info(f"Notification {notification.id} created by {request.user.username}")
            return api_response(
                data=serializer.data,
                message="Notification created successfully",
                status_code=status.HTTP_201_CREATED
            )
        logger.error(f"Notification creation failed: {serializer.errors}")
        return api_response(
            message="Notification creation failed",
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors
        )

class NotificationDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            if request.user.is_authenticated:
                if request.user.profileName.name != "SUPER-ADMIN" and notification.receiver != request.user:
                    logger.warning(f"User {request.user.username} denied access to notification {notification_id}")
                    return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
                serializer = NotificationSerializer(notification)
                logger.info(f"Notification {notification_id} retrieved by {request.user.username}")
                return api_response(data=serializer.data, message="Notification retrieved successfully")
            logger.warning("Unauthenticated user attempted to access notification")
            return api_response(message="Authentication required", status_code=status.HTTP_401_UNAUTHORIZED)
        except Notification.DoesNotExist:
            logger.warning(f"Notification {notification_id} not found")
            return api_response(message="Notification not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            if not request.user.is_authenticated:
                logger.warning("Unauthenticated user attempted to update notification")
                return api_response(message="Authentication required", status_code=status.HTTP_401_UNAUTHORIZED)
            if request.user.profileName.name != "SUPER-ADMIN" and notification.receiver != request.user:
                logger.warning(f"User {request.user.username} denied permission to update notification {notification_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            serializer = NotificationSerializer(notification, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Notification {notification_id} updated by {request.user.username}")
                return api_response(data=serializer.data, message="Notification updated successfully")
            logger.error(f"Notification update failed: {serializer.errors}")
            return api_response(message="Notification update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except Notification.DoesNotExist:
            logger.warning(f"Notification {notification_id} not found")
            return api_response(message="Notification not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, notification_id):
        if not request.user.is_authenticated or request.user.profileName.name != "SUPER-ADMIN":
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to delete notification")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            logger.info(f"Notification {notification_id} deleted by {request.user.username}")
            return api_response(message="Notification deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            logger.warning(f"Notification {notification_id} not found")
            return api_response(message="Notification not found", status_code=status.HTTP_404_NOT_FOUND)