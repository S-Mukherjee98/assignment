from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from .token import get_tokens_for_user
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.permissions import IsAuthenticated
from .producer import send_api_usage_log
from django.contrib.auth import get_user_model
from .throttles import *


User = get_user_model()
class RegisterView(APIView):
    throttle_classes = [RegistrationRateThrottle]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view
class LoginView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code != 200:
                return Response({
                    "success": False,
                    "error": response.data.get("detail", "Invalid credentials.")
                }, status=response.status_code)

            try:
                user = User.objects.get(email=request.data.get("email"))
                user.token_version += 1
                user.save()
            except User.DoesNotExist:
                return Response({
                    "success": False,
                    "error": "User not found."
                }, status=status.HTTP_404_NOT_FOUND)

            tokens = get_tokens_for_user(user)
            return Response({
                "success": True,
                **tokens
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "error": "An unexpected error occurred. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API testing using Postman
class TestView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "API is working"}, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            user = request.user
            user.token_version += 1
            user.save()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class SecureDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        send_api_usage_log(
            event_name="Secure API accessed",
            user_email=request.user.email,
            path=request.path
        )
        return Response({"success":True,"message": "Secure data for you!"})
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = ProfileSerializer(user)

            if not serializer.data:
                return Response({
                    "success": False,
                    "error": "No profile data found."
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "error": "Unable to fetch profile. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            user = request.user
            serializer = ProfileSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Profile updated successfully.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "error": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({
                "success": False,
                "error": "Unable to update profile."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            if not user.check_password(old_password):
                return Response({
                    "success": False,
                    "error": "Old password is incorrect."
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user.set_password(new_password)
                user.save()

                return Response({
                    "success": True,
                    "message": "Password changed successfully."
                }, status=status.HTTP_200_OK)

            except Exception:
                return Response({
                    "success": False,
                    "error": "Something went wrong while changing the password."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "success": False,
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

