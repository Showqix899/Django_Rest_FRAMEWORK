from django.shortcuts import render
from rest_framework.generics import CreateAPIView,GenericAPIView
#Allowany
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import UserSerializers,RegisterSerializers,LoginSerializers
#import authenticate from django
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(CreateAPIView):
    user=User.objects.all()
    serializer_class = RegisterSerializers

class LoginView(GenericAPIView):
    serializer_class=LoginSerializers

    def post(self,request,*args,**kwags):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username,password=password)

        if user is not None:
            refresh=RefreshToken.for_user(user)
            user_serializer=UserSerializers(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user':user_serializer.data
            })
        else:
            return Response({"msg":"Invalid username or password"},status=401)
