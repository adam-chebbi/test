from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from authentication.permissions import IsUser
from payments.models import BankCard
from payments.serializers import BankCardSerializer
from core.utils import api_response
import logging

logger = logging.getLogger('payments')

class BankCardListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request):
        cards = BankCard.objects.filter(userId=request.user, isActive=True)
        serializer = BankCardSerializer(cards, many=True)
        logger.info(f"Retrieved {cards.count()} bank cards for {request.user.username}")
        return api_response(data=serializer.data, message="Bank cards retrieved")

    def post(self, request):
        serializer = BankCardSerializer(data=request.data)
        if serializer.is_valid():
            card = serializer.save()
            if card.userId != request.user:
                card.delete()
                logger.warning(f"User {request.user.username} denied permission")
                return api_response(message="Permission denied", status_code=status.HTTP_403_FORBIDDEN)
            logger.info(f"BankCard {card.id} created by {request.user.username}")
            return api_response(data=serializer.data, message="Bank card created", status_code=status.HTTP_201_CREATED)
        logger.error(f"BankCard creation failed: {serializer.errors}")
        return api_response(message="Creation failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)

class BankCardDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request, card_id):
        try:
            card = BankCard.objects.get(id=card_id, userId=request.user, isActive=True)
            serializer = BankCardSerializer(card)
            logger.info(f"BankCard {card_id} retrieved by {request.user.username}")
            return api_response(data=serializer.data, message="Bank card retrieved")
        except BankCard.DoesNotExist:
            logger.warning(f"BankCard {card_id} not found for {request.user.username}")
            return api_response(message="Not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, card_id):
        try:
            card = BankCard.objects.get(id=card_id, userId=request.user)
            serializer = BankCardSerializer(card, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"BankCard {card_id} updated by {request.user.username}")
                return api_response(data=serializer.data, message="Bank card updated")
            logger.error(f"BankCard update failed: {serializer.errors}")
            return api_response(message="Update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except BankCard.DoesNotExist:
            logger.warning(f"BankCard {card_id} not found")
            return api_response(message="Not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, card_id):
        try:
            card = BankCard.objects.get(id=card_id, userId=request.user)
            card.delete()
            logger.info(f"BankCard {card_id} deleted by {request.user.username}")
            return api_response(message="Bank card deleted", status_code=status.HTTP_204_NO_CONTENT)
        except BankCard.DoesNotExist:
            logger.warning(f"BankCard {card_id} not found")
            return api_response(message="Not found", status_code=status.HTTP_404_NOT_FOUND)