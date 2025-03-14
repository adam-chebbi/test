from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.apps import apps
from core.serializers import DynamicModelSerializer
from core.utils import api_response, paginate_queryset
from authentication.permissions import IsSuperAdmin, IsAdmin, IsModerator, IsUser
import logging

logger = logging.getLogger('core')

class BaseAPIView(APIView):
    def handle_exception(self, exc):
        logger.error(f"Exception in {self.__class__.__name__}: {str(exc)}")
        return api_response(message=str(exc), status_code=status.HTTP_400_BAD_REQUEST, errors={"detail": str(exc)})

class GeneralListView(BaseAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, table, page=None):
        try:
            model_map = {
                'user': 'authentication.User', 'profile': 'authentication.Profile', 'login': 'authentication.Login',
                'session': 'authentication.Session', 'bankcard': 'payments.BankCard', 'product': 'products.Product',
                'productitem': 'products.ProductItem', 'pricebook': 'products.PriceBook', 'shoppingcart': 'orders.ShoppingCart',
                'case': 'orders.Case', 'notification': 'notifications.Notification', 'recordtype': 'records.RecordType',
                'address': 'records.Address'
            }
            if table.lower() not in model_map:
                logger.warning(f"Invalid table name: {table}")
                return api_response(message="Invalid table name", status_code=status.HTTP_400_BAD_REQUEST)

            model = apps.get_model(model_map[table.lower()])
            filters = request.data.get('filters', {})
            queryset = model.objects.all()

            # Apply permission-based filtering
            if not request.user.is_authenticated or request.user.profileName.name != "SUPER-ADMIN":
                if table.lower() == 'user' and not IsAdmin().has_permission(request, self):
                    return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
                elif table.lower() == 'profile' and not IsSuperAdmin().has_permission(request, self):
                    return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
                elif table.lower() in ['shoppingcart', 'notification']:
                    key = 'userId' if table.lower() == 'shoppingcart' else 'receiver'
                    filters[key] = request.user
                elif table.lower() == 'productitem':
                    filters['shoppingCartId__userId'] = request.user
                elif table.lower() == 'case' and not IsModerator().has_permission(request, self):
                    filters['accountId'] = request.user

            try:
                queryset = queryset.filter(**filters)
            except Exception as e:
                logger.error(f"Invalid filter parameters for {table}: {str(e)}")
                return api_response(message="Invalid filter parameters", status_code=status.HTTP_400_BAD_REQUEST, errors={"detail": str(e)})

            paginated_data = paginate_queryset(queryset, request)
            serializer = DynamicModelSerializer(paginated_data['results'], many=True, model=model)
            logger.info(f"Retrieved list for {table} with {paginated_data['count']} items")
            return api_response(
                data={"results": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
                message=f"{table.capitalize()} list retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error retrieving list for {table}: {str(e)}")
            return api_response(message="Error retrieving list", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, errors={"detail": str(e)})

class GeneralDetailView(BaseAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, table, id):
        try:
            model_map = {
                'user': 'authentication.User', 'profile': 'authentication.Profile', 'login': 'authentication.Login',
                'session': 'authentication.Session', 'bankcard': 'payments.BankCard', 'product': 'products.Product',
                'productitem': 'products.ProductItem', 'pricebook': 'products.PriceBook', 'shoppingcart': 'orders.ShoppingCart',
                'case': 'orders.Case', 'notification': 'notifications.Notification', 'recordtype': 'records.RecordType',
                'address': 'records.Address'
            }
            if table.lower() not in model_map:
                logger.warning(f"Invalid table name: {table}")
                return api_response(message="Invalid table name", status_code=status.HTTP_400_BAD_REQUEST)

            model = apps.get_model(model_map[table.lower()])
            instance = model.objects.get(id=id)

            # Permission checks
            if request.user.is_authenticated and request.user.profileName.name != "SUPER-ADMIN":
                if table.lower() == 'user' and not IsAdmin().has_permission(request, self):
                    return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
                elif table.lower() == 'profile':
                    return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
                elif table.lower() == 'shoppingcart' and instance.userId != request.user:
                    return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
                elif table.lower() == 'notification' and instance.receiver != request.user:
                    return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
                elif table.lower() == 'productitem' and instance.shoppingCartId.userId != request.user:
                    return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
                elif table.lower() == 'case' and not IsModerator().has_permission(request, self) and instance.accountId != request.user:
                    return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)

            serializer = DynamicModelSerializer(instance, model=model)
            logger.info(f"Retrieved detail for {table} with id {id}")
            return api_response(data=serializer.data, message=f"{table.capitalize()} detail retrieved successfully")
        except model.DoesNotExist:
            logger.warning(f"{table.capitalize()} with id {id} not found")
            return api_response(message=f"{table.capitalize()} not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving detail for {table} with id {id}: {str(e)}")
            return api_response(message="Error retrieving detail", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, errors={"detail": str(e)})