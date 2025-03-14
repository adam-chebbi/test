from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from authentication.permissions import IsUser, IsModerator, IsAdmin
from orders.models import ShoppingCart, Case
from orders.serializers import ShoppingCartSerializer, CaseSerializer
from core.utils import api_response, paginate_queryset
import logging

logger = logging.getLogger('orders')

class ShoppingCartListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request):
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user attempted to access shopping carts")
            return api_response(message="Authentication required", status_code=status.HTTP_401_UNAUTHORIZED)
        if IsAdmin().has_permission(request, self):
            carts = ShoppingCart.objects.filter(isActive=True)
        else:
            carts = ShoppingCart.objects.filter(userId=request.user, isActive=True)
        paginated_data = paginate_queryset(carts, request)
        serializer = ShoppingCartSerializer(paginated_data['results'], many=True)
        logger.info(f"Retrieved {paginated_data['count']} shopping carts for {request.user.username}")
        return api_response(
            data={"shopping_carts": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
            message="Shopping carts retrieved successfully"
        )

    def post(self, request):
        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid():
            cart = serializer.save()
            if cart.userId != request.user and not IsAdmin().has_permission(request, self):
                cart.delete()
                logger.warning(f"User {request.user.username} denied permission to create cart for another user")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            logger.info(f"ShoppingCart {cart.id} created by {request.user.username}")
            return api_response(data=serializer.data, message="Shopping cart created successfully", status_code=status.HTTP_201_CREATED)
        logger.error(f"ShoppingCart creation failed: {serializer.errors}")
        return api_response(message="Shopping cart creation failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class ShoppingCartDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request, cart_id):
        try:
            cart = ShoppingCart.objects.get(id=cart_id, isActive=True)
            if cart.userId != request.user and not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied access to cart {cart_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            serializer = ShoppingCartSerializer(cart)
            logger.info(f"ShoppingCart {cart_id} retrieved by {request.user.username}")
            return api_response(data=serializer.data, message="Shopping cart retrieved successfully")
        except ShoppingCart.DoesNotExist:
            logger.warning(f"ShoppingCart {cart_id} not found")
            return api_response(message="Shopping cart not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, cart_id):
        try:
            cart = ShoppingCart.objects.get(id=cart_id)
            if cart.userId != request.user and not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied permission to update cart {cart_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            serializer = ShoppingCartSerializer(cart, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"ShoppingCart {cart_id} updated by {request.user.username}")
                return api_response(data=serializer.data, message="Shopping cart updated successfully")
            logger.error(f"ShoppingCart update failed: {serializer.errors}")
            return api_response(message="Shopping cart update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except ShoppingCart.DoesNotExist:
            logger.warning(f"ShoppingCart {cart_id} not found")
            return api_response(message="Shopping cart not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, cart_id):
        try:
            cart = ShoppingCart.objects.get(id=cart_id)
            if cart.userId != request.user and not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied permission to delete cart {cart_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            cart.delete()
            logger.info(f"ShoppingCart {cart_id} deleted by {request.user.username}")
            return api_response(message="Shopping cart deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except ShoppingCart.DoesNotExist:
            logger.warning(f"ShoppingCart {cart_id} not found")
            return api_response(message="Shopping cart not found", status_code=status.HTTP_404_NOT_FOUND)

class CaseListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user attempted to access cases")
            return api_response(message="Authentication required", status_code=status.HTTP_401_UNAUTHORIZED)
        if IsModerator().has_permission(request, self):
            cases = Case.objects.filter(isActive=True)
        else:
            cases = Case.objects.filter(accountId=request.user, isActive=True)
        paginated_data = paginate_queryset(cases, request)
        serializer = CaseSerializer(paginated_data['results'], many=True)
        logger.info(f"Retrieved {paginated_data['count']} cases for {request.user.username}")
        return api_response(
            data={"cases": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
            message="Cases retrieved successfully"
        )

    def post(self, request):
        serializer = CaseSerializer(data=request.data)
        if serializer.is_valid():
            case = serializer.save()
            if case.accountId != request.user and not IsModerator().has_permission(request, self):
                case.delete()
                logger.warning(f"User {request.user.username} denied permission to create case for another user")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            logger.info(f"Case {case.id} created by {request.user.username}")
            return api_response(data=serializer.data, message="Case created successfully", status_code=status.HTTP_201_CREATED)
        logger.error(f"Case creation failed: {serializer.errors}")
        return api_response(message="Case creation failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class CaseDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, case_id):
        try:
            case = Case.objects.get(id=case_id, isActive=True)
            if case.accountId != request.user and not IsModerator().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied access to case {case_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            serializer = CaseSerializer(case)
            logger.info(f"Case {case_id} retrieved by {request.user.username}")
            return api_response(data=serializer.data, message="Case retrieved successfully")
        except Case.DoesNotExist:
            logger.warning(f"Case {case_id} not found")
            return api_response(message="Case not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, case_id):
        try:
            case = Case.objects.get(id=case_id)
            if case.accountId != request.user and not IsModerator().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied permission to update case {case_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            serializer = CaseSerializer(case, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Case {case_id} updated by {request.user.username}")
                return api_response(data=serializer.data, message="Case updated successfully")
            logger.error(f"Case update failed: {serializer.errors}")
            return api_response(message="Case update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except Case.DoesNotExist:
            logger.warning(f"Case {case_id} not found")
            return api_response(message="Case not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, case_id):
        try:
            case = Case.objects.get(id=case_id)
            if not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied permission to delete case {case_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            case.delete()
            logger.info(f"Case {case_id} deleted by {request.user.username}")
            return api_response(message="Case deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except Case.DoesNotExist:
            logger.warning(f"Case {case_id} not found")
            return api_response(message="Case not found", status_code=status.HTTP_404_NOT_FOUND)