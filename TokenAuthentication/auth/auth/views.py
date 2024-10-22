from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UserSerializers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,TokenAuthentication




@api_view(['POST'])
def loginUser(request):
    user=get_object_or_404(User,username=request.data['username'])
    
    if not user.check_password(request.data['password']):
        return Response({'error':'Invalid password'},status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer=UserSerializers(instance=user)
    return Response({'token':token.key,"user":serializer.data},status=status.HTTP_200_OK)



@api_view(['POST'])
def signUpUser(request):
    serializer=UserSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user=User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token=Token.objects.create(user=user)
        return Response({'token':token.key,"user":serializer.data},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"passed for {}".format(request.user.email)})