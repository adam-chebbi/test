from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from authentication.permissions import IsSuperAdmin, IsAdmin, IsModerator, IsUser
from authentication.serializers import UserSerializer, LoginSerializer, SessionSerializer, ProfileSerializer
from authentication.models import Profile
from core.utils import api_response, paginate_queryset
import logging

logger = logging.getLogger('authentication')

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User {user.username} registered successfully")
            return api_response(
                data={'id': user.id, 'username': user.username},
                message="User created successfully",
                status_code=status.HTTP_201_CREATED
            )
        logger.error(f"User registration failed: {serializer.errors}")
        return api_response(
            message="User creation failed",
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors
        )

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = serializer.validated_data['token']
            logger.info(f"User {user.username} logged in successfully")
            return api_response(
                data={'token': token, 'user_id': user.id},
                message="Login successful",
                status_code=status.HTTP_200_OK
            )
        logger.error(f"Login failed: {serializer.errors}")
        return api_response(
            message="Login failed",
            status_code=status.HTTP_401_UNAUTHORIZED,
            errors=serializer.errors
        )

class SessionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            session = serializer.save()
            logger.info(f"Session {session.code} created by {request.user.username}")
            return api_response(
                data=serializer.data,
                message="Session created successfully",
                status_code=status.HTTP_201_CREATED
            )
        logger.error(f"Session creation failed: {serializer.errors}")
        return api_response(
            message="Session creation failed",
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors
        )

class ProfileListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        profiles = Profile.objects.all()
        paginated_data = paginate_queryset(profiles, request)
        serializer = ProfileSerializer(paginated_data['results'], many=True)
        return api_response(
            data={"profiles": serializer.data, "count": paginated_data['count'], "next": paginated_data['next'], "previous": paginated_data['previous']},
            message="Profiles retrieved successfully"
        )

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            logger.info(f"Profile {profile.name} created by {request.user.username}")
            return api_response(
                data=serializer.data,
                message="Profile created successfully",
                status_code=status.HTTP_201_CREATED
            )
        logger.error(f"Profile creation failed: {serializer.errors}")
        return api_response(
            message="Profile creation failed",
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors
        )

class ProfileDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperAdmin]

    def get(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
            serializer = ProfileSerializer(profile)
            return api_response(data=serializer.data, message="Profile retrieved successfully")
        except Profile.DoesNotExist:
            return api_response(message="Profile not found", status_code=status.HTTP_404_NOT_FOUND)

    def put(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Profile {profile.name} updated by {request.user.username}")
                return api_response(data=serializer.data, message="Profile updated successfully")
            logger.error(f"Profile update failed: {serializer.errors}")
            return api_response(message="Profile update failed", status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)
        except Profile.DoesNotExist:
            return api_response(message="Profile not found", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
            profile.delete()
            logger.info(f"Profile {profile_id} deleted by {request.user.username}")
            return api_response(message="Profile deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist:
            return api_response(message="Profile not found", status_code=status.HTTP_404_NOT_FOUND)