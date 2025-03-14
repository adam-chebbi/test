from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from authentication.permissions import IsAdmin, IsUser
from products.models import Product, PriceBook, ProductItem
from products.serializers import ProductSerializer, PriceBookSerializer, ProductItemSerializer
from core.utils import api_response, paginate_queryset
import logging

logger = logging.getLogger('products')

class ProductListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(isActive=True)
        paginated_data = paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_data['results'], many=True)
        logger.info(f"Retrieved {paginated_data['count']} products")
        return api_response(
            data={"products": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
            message="Products retrieved successfully"
        )

    def post(self, request):
        if not request.user.is_authenticated or not IsAdmin().has_permission(request, self):
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to create product")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            logger.info(f"Product {product.id} created by {request.user.username}")
            return api_response(data=serializer.data, message="Product created successfully", status_code=status.HTTP_201_CREATED)
        logger.error(f"Product creation failed: {serializer.errors}")
        return api_response(message="Product creation failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class ProductDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id, isActive=True)
            serializer = ProductSerializer(product)
            logger.info(f"Product {product_id} retrieved")
            return api_response(data=serializer.data, message="Product retrieved successfully")
        except Product.DoesNotExist:
            logger.warning(f"Product {product_id} not found")
            return api_response(message="Product not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, product_id):
        if not request.user.is_authenticated or not IsAdmin().has_permission(request, self):
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to update product")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Product {product_id} updated by {request.user.username}")
                return api_response(data=serializer.data, message="Product updated successfully")
            logger.error(f"Product update failed: {serializer.errors}")
            return api_response(message="Product update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except Product.DoesNotExist:
            logger.warning(f"Product {product_id} not found")
            return api_response(message="Product not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        if not request.user.is_authenticated or not IsAdmin().has_permission(request, self):
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to delete product")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            logger.info(f"Product {product_id} deleted by {request.user.username}")
            return api_response(message="Product deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            logger.warning(f"Product {product_id} not found")
            return api_response(message="Product not found", status_code=status.HTTP_404_NOT_FOUND)

class PriceBookListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        pricebooks = PriceBook.objects.filter(isActive=True)
        paginated_data = paginate_queryset(pricebooks, request)
        serializer = PriceBookSerializer(paginated_data['results'], many=True)
        logger.info(f"Retrieved {paginated_data['count']} pricebooks")
        return api_response(
            data={"pricebooks": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
            message="PriceBooks retrieved successfully"
        )

    def post(self, request):
        if not request.user.is_authenticated or not IsAdmin().has_permission(request, self):
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to create pricebook")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        serializer = PriceBookSerializer(data=request.data)
        if serializer.is_valid():
            pricebook = serializer.save()
            logger.info(f"PriceBook {pricebook.id} created by {request.user.username}")
            return api_response(data=serializer.data, message="PriceBook created successfully", status_code=status.HTTP_201_CREATED)
        logger.error(f"PriceBook creation failed: {serializer.errors}")
        return api_response(message="PriceBook creation failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class PriceBookDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, pricebook_id):
        try:
            pricebook = PriceBook.objects.get(id=pricebook_id, isActive=True)
            serializer = PriceBookSerializer(pricebook)
            logger.info(f"PriceBook {pricebook_id} retrieved")
            return api_response(data=serializer.data, message="PriceBook retrieved successfully")
        except PriceBook.DoesNotExist:
            logger.warning(f"PriceBook {pricebook_id} not found")
            return api_response(message="PriceBook not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, pricebook_id):
        if not request.user.is_authenticated or not IsAdmin().has_permission(request, self):
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to update pricebook")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        try:
            pricebook = PriceBook.objects.get(id=pricebook_id)
            serializer = PriceBookSerializer(pricebook, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"PriceBook {pricebook_id} updated by {request.user.username}")
                return api_response(data=serializer.data, message="PriceBook updated successfully")
            logger.error(f"PriceBook update failed: {serializer.errors}")
            return api_response(message="PriceBook update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except PriceBook.DoesNotExist:
            logger.warning(f"PriceBook {pricebook_id} not found")
            return api_response(message="PriceBook not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pricebook_id):
        if not request.user.is_authenticated or not IsAdmin().has_permission(request, self):
            logger.warning(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} denied permission to delete pricebook")
            return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
        try:
            pricebook = PriceBook.objects.get(id=pricebook_id)
            pricebook.delete()
            logger.info(f"PriceBook {pricebook_id} deleted by {request.user.username}")
            return api_response(message="PriceBook deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except PriceBook.DoesNotExist:
            logger.warning(f"PriceBook {pricebook_id} not found")
            return api_response(message="PriceBook not found", status_code=status.HTTP_404_NOT_FOUND)

class ProductItemListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request):
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user attempted to access product items")
            return api_response(message="Authentication required", status_code=status.HTTP_401_UNAUTHORIZED)
        product_items = ProductItem.objects.filter(shoppingCartId__userId=request.user, isActive=True)
        paginated_data = paginate_queryset(product_items, request)
        serializer = ProductItemSerializer(paginated_data['results'], many=True)
        logger.info(f"Retrieved {paginated_data['count']} product items for {request.user.username}")
        return api_response(
            data={"product_items": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
            message="Product items retrieved successfully"
        )

    def post(self, request):
        serializer = ProductItemSerializer(data=request.data)
        if serializer.is_valid():
            product_item = serializer.save()
            if product_item.shoppingCartId.userId != request.user and not IsAdmin().has_permission(request, self):
                product_item.delete()
                logger.warning(f"User {request.user.username} denied permission to add to cart {product_item.shoppingCartId.id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            logger.info(f"ProductItem {product_item.id} created by {request.user.username}")
            return api_response(data=serializer.data, message="Product item created successfully", status_code=status.HTTP_201_CREATED)
        logger.error(f"ProductItem creation failed: {serializer.errors}")
        return api_response(message="Product item creation failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class ProductItemDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request, productitem_id):
        try:
            product_item = ProductItem.objects.get(id=productitem_id, isActive=True)
            if product_item.shoppingCartId.userId != request.user and not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied access to product item {productitem_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            serializer = ProductItemSerializer(product_item)
            logger.info(f"ProductItem {productitem_id} retrieved by {request.user.username}")
            return api_response(data=serializer.data, message="Product item retrieved successfully")
        except ProductItem.DoesNotExist:
            logger.warning(f"ProductItem {productitem_id} not found")
            return api_response(message="Product item not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, productitem_id):
        try:
            product_item = ProductItem.objects.get(id=productitem_id)
            if product_item.shoppingCartId.userId != request.user and not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied permission to update product item {productitem_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            serializer = ProductItemSerializer(product_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"ProductItem {productitem_id} updated by {request.user.username}")
                return api_response(data=serializer.data, message="Product item updated successfully")
            logger.error(f"ProductItem update failed: {serializer.errors}")
            return api_response(message="Product item update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except ProductItem.DoesNotExist:
            logger.warning(f"ProductItem {productitem_id} not found")
            return api_response(message="Product item not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, productitem_id):
        try:
            product_item = ProductItem.objects.get(id=productitem_id)
            if product_item.shoppingCartId.userId != request.user and not IsAdmin().has_permission(request, self):
                logger.warning(f"User {request.user.username} denied permission to delete product item {productitem_id}")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            product_item.delete()
            logger.info(f"ProductItem {productitem_id} deleted by {request.user.username}")
            return api_response(message="Product item deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except ProductItem.DoesNotExist:
            logger.warning(f"ProductItem {productitem_id} not found")
            return api_response(message="Product item not found", status_code=status.HTTP_404_NOT_FOUND)