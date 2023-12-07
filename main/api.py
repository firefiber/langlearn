from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import NewUserSerializer


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Session ID is automatically set in the cookie
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Logged out successfully'})


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api.py or views.py
class RefillSentencesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        new_sentences = self.get_additional_sentences_for_user(user)
        return Response({'new_sentences': new_sentences})

    def get_additional_sentences_for_user(self, user):
        # Logic to generate additional sentences
        return [
            {'sentence': 'New example sentence', 'translation': 'New translation'},
            # ... other sentences
        ]


class SessionDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # Logic to gather user info and sentence/translation pairs
        user_info = {
            'username': user.username,
            'level': user.userprofile.proficiency_level,  # Example
            # Add other non-sensitive user info
        }
        sentences = self.get_sentences_for_user(user)

        return Response({
            'user_info': user_info,
            'sentences': sentences
        })

    def get_sentences_for_user(self, user):
        # Custom logic to generate sentence/translation pairs
        # This might involve querying your database based on user's language proficiency
        return [
            {'sentence': 'Example sentence', 'translation': 'Example translation'},
            # ... other sentences
        ]