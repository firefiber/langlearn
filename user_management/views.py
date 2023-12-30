from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserDetailSerializer, UserTrainingDataSerializer
from .models import UserProfile

class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            csrf_token = get_token(request)
            print(csrf_token)
            return Response({
                'detail': 'Login successful',
                'csrfToken': csrf_token
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class CustomLoginView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             # Check if the user account is active
#             if not user.is_active:
#                 return Response({'detail': 'Account not active'}, status=status.HTTP_403_FORBIDDEN)
#
#             try:
#                 user_profile = UserProfile.objects.get(user=user)
#             except UserProfile.DoesNotExist:
#                 return Response({"error": "UserProfile not found"}, status=404)
#
#             login(request, user)  # Log in the user
#             serializer = UserDetailSerializer(user_profile)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Logged out successfully'})


class CustomSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return Response({
            'detail': 'User is authenticated',
            'csrfToken': csrf_token
        }, status=status.HTTP_200_OK)

class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserDetailSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"error": "UserProfile not found"}, status=404)

class UserTrainingDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            active_language_proficiency = user_profile.get_active_language_proficiency()
            if active_language_proficiency:
                serializer = UserTrainingDataSerializer(active_language_proficiency)
                return Response(serializer.data)
            else:
                return Response({"error": "Active language proficiency not found"}, status=404)
        except UserProfile.DoesNotExist:
            return Response({"error": "UserProfile not found"}, status=404)

# class UserRegistrationView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request, *args, **kwargs):
#         with transaction.atomic():
#             serializer = UserRegistrationSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

