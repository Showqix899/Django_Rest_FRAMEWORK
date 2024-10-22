from rest_framework  import serializers
from django.contrib.auth.models import User
from .models import Book


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','password']
        extra_kwargs={"password":{"write_only":True}}


    def create(self, validated_data):
        user=User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class Bookserializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'