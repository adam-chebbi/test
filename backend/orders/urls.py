from django.urls import path
from orders.views import ShoppingCartListCreateView, ShoppingCartDetailView, CaseListCreateView, CaseDetailView

urlpatterns = [
    path('shoppingcarts/', ShoppingCartListCreateView.as_view(), name='shoppingcart-list-create'),
    path('shoppingcarts/<str:cart_id>/', ShoppingCartDetailView.as_view(), name='shoppingcart-detail'),
    path('cases/', CaseListCreateView.as_view(), name='case-list-create'),
    path('cases/<str:case_id>/', CaseDetailView.as_view(), name='case-detail'),
]