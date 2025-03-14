from django.urls import path
from payments.views import BankCardListCreateView, BankCardDetailView

urlpatterns = [
    path('bankcards/', BankCardListCreateView.as_view(), name='bankcard-list-create'),
    path('bankcards/<str:card_id>/', BankCardDetailView.as_view(), name='bankcard-detail'),
]