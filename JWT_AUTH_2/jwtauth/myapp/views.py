from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Book
from .serializer import Bookserializer,UserSerializer
from rest_framework import generics,permissions
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        if user.check_password(request.data['password']):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=400)

    
class BooklistCreateView(generics.ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=Bookserializer
    permission_classes=[permissions.IsAuthenticated]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Book.objects.all()
    serializer_class=Bookserializer
    permission_classes=[permissions.IsAuthenticated]

