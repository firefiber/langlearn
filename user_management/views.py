# from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import never_cache
# from django.views.generic.edit import FormView
#
# from .forms import NewUserForm
#
# # def register(request):
# #     if request.method == 'POST':
# #         user_form = NewUserForm(request.POST)
# #
# #         if user_form.is_valid():
# #             user = user_form.save()
# #             profile = profile_form.save(commit=False)
# #             profile.user = user
# #             profile.save()
# #             return redirect('login')
# #     else:
# #         user_form = UserForm()
# #         profile_form = UserProfileForm()
# #
# #     return render(request, 'user_management/register.html', {'user_form': user_form, 'profile_form': profile_form})
#
# class RegisterView(FormView):
#     template_name = 'user_management/register.html'
#     form_class = NewUserForm
#     success_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#
#     @method_decorator(never_cache)
#     def dispatch(self, *args, **kwargs):
#         return super(RegisterView, self).dispatch(*args, **kwargs)

from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer


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
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

