from django.urls import path
from records.views import RecordTypeListCreateView, RecordTypeDetailView, AddressListCreateView, AddressDetailView

urlpatterns = [
    path('recordtypes/', RecordTypeListCreateView.as_view(), name='recordtype-list-create'),
    path('recordtypes/<str:recordtype_id>/', RecordTypeDetailView.as_view(), name='recordtype-detail'),
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<str:address_id>/', AddressDetailView.as_view(), name='address-detail'),
]