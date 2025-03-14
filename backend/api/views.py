from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class AdminSessionView(APIView):
    def get(self, request):
        return Response({"message": "Admin session data"})

class UserSessionView(APIView):
    def get(self, request):
        return Response({"message": "User session data"})