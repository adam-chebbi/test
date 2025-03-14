from rest_framework import serializers
from authentication.models import User, Login, Profile, Session
from django.contrib.auth.hashers import make_password, check_password
import jwt
from django.conf import settings
from datetime import datetime, timedelta
import random
import string

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'email', 'username', 'profileName', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile_name = validated_data.pop('profileName', 'USER')
        if isinstance(profile_name, str):
            profile, _ = Profile.objects.get_or_create(name=profile_name)
        else:
            profile = profile_name
        user = User(
            **validated_data,
            username=validated_data.get('username', validated_data['email'].split('@')[0]),
            profileName=profile
        )
        user.save()
        # Create Login entry
        Login.objects.create(
            userId=user,
            token1=make_password(validated_data['email'] + password),
            token2=make_password(user.username + password)
        )
        return user

class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email_or_username = data.get('email_or_username')
        password = data.get('password')

        try:
            if '@' in email_or_username:
                user = User.objects.get(email=email_or_username)
                login = Login.objects.filter(userId=user, isActive=True).first()
                if not login or not check_password(email_or_username + password, login.token1):
                    raise serializers.ValidationError("Invalid credentials")
            else:
                user = User.objects.get(username=email_or_username)
                login = Login.objects.filter(userId=user, isActive=True).first()
                if not login or not check_password(email_or_username + password, login.token2):
                    raise serializers.ValidationError("Invalid credentials")

            if not user.isActive:
                raise serializers.ValidationError("Account is deactivated")

            jwt_token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm='HS256')

            return {'user': user, 'token': jwt_token}
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'code', 'action', 'isActive', 'createdDate']
        read_only_fields = ['id', 'code', 'createdDate']

    def create(self, validated_data):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Session.objects.filter(code=code).exists():
                break
        session = Session(code=code, **validated_data)
        session.save()
        return session

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'createdDate', 'lastModifiedDate', 'createdById', 'lastModifiedById']
        read_only_fields = ['id', 'createdDate', 'lastModifiedDate']