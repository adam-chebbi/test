from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from authentication.permissions import IsUser, IsAdmin
from records.models import RecordType, Address
from records.serializers import RecordTypeSerializer, AddressSerializer
from core.utils import api_response, paginate_queryset
import logging

logger = logging.getLogger('records')

class RecordTypeListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        record_types = RecordType.objects.filter(isActive=True)
        paginated_data = paginate_queryset(record_types, request)
        serializer = RecordTypeSerializer(paginated_data['results'], many=True)
        logger.info(f"Retrieved {paginated_data['count']} record types")
        return api_response(
            data={"record_types": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
            message="Record types retrieved successfully"
        )

    def post(self, request):
        if not request.user.is_authenticated or not IsAdmin().has_permission(request, self):
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to create record type")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        serializer = RecordTypeSerializer(data=request.data)
        if serializer.is_valid():
            record_type = serializer.save()
            logger.info(f"RecordType {record_type.id} created by {request.user.username}")
            return api_response(data=serializer.data, message="Record type created successfully", status_code=status.HTTP_201_CREATED)
        logger.error(f"RecordType creation failed: {serializer.errors}")
        return api_response(message="Record type creation failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class RecordTypeDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, recordtype_id):
        try:
            record_type = RecordType.objects.get(id=recordtype_id, isActive=True)
            serializer = RecordTypeSerializer(record_type)
            logger.info(f"RecordType {recordtype_id} retrieved")
            return api_response(data=serializer.data, message="Record type retrieved successfully")
        except RecordType.DoesNotExist:
            logger.warning(f"RecordType {recordtype_id} not found")
            return api_response(message="Record type not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, recordtype_id):
        if not request.user.is_authenticated or not IsAdmin().has_permission(request, self):
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to update record type")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        try:
            record_type = RecordType.objects.get(id=recordtype_id)
            serializer = RecordTypeSerializer(record_type, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"RecordType {recordtype_id} updated by {request.user.username}")
                return api_response(data=serializer.data, message="Record type updated successfully")
            logger.error(f"RecordType update failed: {serializer.errors}")
            return api_response(message="Record type update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except RecordType.DoesNotExist:
            logger.warning(f"RecordType {recordtype_id} not found")
            return api_response(message="Record type not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, recordtype_id):
        if not request.user.is_authenticated or not IsAdmin().has_permission(request, self):
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to delete record type")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        try:
            record_type = RecordType.objects.get(id=recordtype_id)
            record_type.delete()
            logger.info(f"RecordType {recordtype_id} deleted by {request.user.username}")
            return api_response(message="Record type deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except RecordType.DoesNotExist:
            logger.warning(f"RecordType {recordtype_id} not found")
            return api_response(message="Record type not found", status_code=status.HTTP_404_NOT_FOUND)

class AddressListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request):
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user attempted to access addresses")
            return api_response(message="Authentication required", status_code=status.HTTP_401_UNAUTHORIZED)
        if IsAdmin().has_permission(request, self):
            addresses = Address.objects.filter(isActive=True)
        else:
            addresses = Address.objects.filter(userId=request.user, isActive=True)
        paginated_data = paginate_queryset(addresses, request)
        serializer = AddressSerializer(paginated_data['results'], many=True)
        logger.info(f"Retrieved {paginated_data['count']} addresses for {request.user.username}")
        return api_response(
            data={"addresses": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
            message="Addresses retrieved successfully"
        )

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.save()
            if address.userId != request.user and not IsAdmin().has_permission(request, self):
                address.delete()
                logger.warning(f"User {request.user.username} denied permission to create address for another user")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            logger.info(f"Address {address.id} created by {request.user.username}")
            return api_response(data=serializer.data, message="Address created successfully", status_code=status.HTTP_201_CREATED)
        logger.error(f"Address creation failed: {serializer.errors}")
        return api_response(message="Address creation failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class AddressDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id, isActive=True)
            if address.userId != request.user and not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied access to address {address_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            serializer = AddressSerializer(address)
            logger.info(f"Address {address_id} retrieved by {request.user.username}")
            return api_response(data=serializer.data, message="Address retrieved successfully")
        except Address.DoesNotExist:
            logger.warning(f"Address {address_id} not found")
            return api_response(message="Address not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            if address.userId != request.user and not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied permission to update address {address_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Address {address_id} updated by {request.user.username}")
                return api_response(data=serializer.data, message="Address updated successfully")
            logger.error(f"Address update failed: {serializer.errors}")
            return api_response(message="Address update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except Address.DoesNotExist:
            logger.warning(f"Address {address_id} not found")
            return api_response(message="Address not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            if address.userId != request.user and not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied permission to delete address {address_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            address.delete()
            logger.info(f"Address {address_id} deleted by {request.user.username}")
            return api_response(message="Address deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            logger.warning(f"Address {address_id} not found")
            return api_response(message="Address not found", status_code=status.HTTP_404_NOT_FOUND)