from rest_framework import serializers
from .models import User,UserManager
from rest_framework.serializers import ModelSerializer
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator 


#Serializer for User Details

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = ('id','full_name','email','photo','username','date_joined','active','admin',)


#Serializer for New User-Registeration 

class UserRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False,default='')
    email     = serializers.EmailField(required=True)
    password  = serializers.CharField(required=True,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    photo     = serializers.ImageField(required=False)
    username  = serializers.CharField(required=False)
      
    class Meta:
        model  = User
        fields = ['id','full_name','email','photo','username','password','password2']


#Serializer for User-Login

class UserLoginSerializer(serializers.Serializer):
    email    = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type':'password'},max_length=200,write_only=True,required=True)
    
    def validate(self, data):
        email    = data.get('email','')
        password = data.get('password','')
                                           
        
        if email and password:
            user = authenticate(email=email, password=password)
              
            if user:
                if user.is_active:
                    data['user']= user
                else:
                    raise exceptions.ValidationError({"status":'failed',
                                                      "message" : 'User is not active',
                                                      "data": []})  
            else:
                raise exceptions.ValidationError({"status":'failed',
                                                  "message" : 'Wrong Email-ID or Password ',
                                                  "data": []})    
        else:
            raise exceptions.ValidationError({"status":'failed',
                                              "message" : 'Invalid Credentials',
                                              "data": []})    
  
                             
        return data 


#Serializer for Updating User Profile

class UserEditSerializer(serializers.ModelSerializer):
    photo     = serializers.ImageField(required=False)
    full_name = serializers.CharField(required=False)
    username  = serializers.CharField(required=False)

    class Meta:
        model            = User
        fields           = ('id','full_name','email','photo','username','date_joined','active','admin',)
        read_only_fields = ('id','email','date_joined','active','admin',)