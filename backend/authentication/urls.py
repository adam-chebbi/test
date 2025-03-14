from django.urls import path
from authentication.views import RegisterView, LoginView, SessionView, ProfileListCreateView, ProfileDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('session/', SessionView.as_view(), name='session'),
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<str:profile_id>/', ProfileDetailView.as_view(), name='profile-detail'),
]