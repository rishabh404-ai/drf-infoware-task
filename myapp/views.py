from .models import User,UserManager
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, generics
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib import auth
from django.contrib.auth.models import auth
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
from .serializers import (UserSerializer,
                          UserRegisterSerializer,
                          UserLoginSerializer,
                          UserEditSerializer 
                         )  


#Api for User-Registeration 

class UserRegisterAPIView(generics.GenericAPIView):
  """
  REST API making a POST request for registering a User. 
  """

  serializer_class   = UserRegisterSerializer
  permission_classes = [AllowAny,]


  def post(self,request):
    serializer = self.serializer_class(request.data) 

    full_name  = request.data['full_name']
    email      = request.data['email']
    password   = request.data['password']
    password2  = request.data['password2'] 
    photo      = request.data['photo']
    username   = request.data['username']

    if User.objects.filter(email=email).exists():
        raise ValidationError({"status":'failed',
                               "message" : 'This Email-ID is already taken !',
                               "data": []})

    if password != password2:
        raise ValidationError({"status":'failed',
                               "message" : 'Passwords are not matching !',
                               "data": []})
    if not email:
        raise ValidationError({"status":'failed',
                               "message" : 'Please enter a valid email !',
                               "data": []})
    if not password:
        raise ValidationError({"status":'failed',
                               "message" : 'Please enter password !',
                               "data": []})  

    try:     
      user = User.objects.create_user(full_name=full_name,email=email,password=password,photo=photo,username=username)
      user.save()
      return Response({"status":'success',
                       "message" :'Registration Successful',
                       "data":serializer.data},status=status.HTTP_201_CREATED)

    except Exception as e:
        raise ValidationError({'status': 'failed',
                              'message':'Something went wrong. Please try again !',
                              'data':[]})  
   
      

#Api for User-Login

class UserLoginAPIView(generics.GenericAPIView):
  """
  REST API making a POST request for login a User. 
  """
  
  serializer_class = UserLoginSerializer
  
  def post(self, request):
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=False):
      raise ValidationError({'status':'failed',
                             'message':'Invalid Email or Password',
                             'data':[]})
                              
    user = serializer.validated_data['user']
    auth.login(request,user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'status':'success',
                     'message':'Login Successful',
                     'Token': token.key},status=status.HTTP_200_OK)
  

#Api for User-Logout

class UserLogoutView(APIView):
   """
   REST API making a POST request for registering a User. 
   """
   
   authentication_classes = [TokenAuthentication,]
   permission_classes     = [IsAuthenticated,]

   def post(self,request):
    
    try:
      request.user.auth_token.delete()
      auth.logout(request)
            
      return Response({'status':'success',
                       'message':'Successfully Logged Out'},status=status.HTTP_200_OK)

    except:
        raise ValidationError({'status':'failed',
                               'message':'Invalid Token',
                               'data':[]})  


#Api for User-Profile-Details

class UserDetailsAPIView(generics.GenericAPIView):
  """
  REST API making a GET request for fetching User Details. 
  """

  serializer_class       = UserSerializer
  authentication_classes = [TokenAuthentication,]
  permission_classes     = [IsAuthenticated,]

  def get(self, request, *args, **kwargs):
     
    user = UserSerializer(request.user)
    return Response(user.data)



#Api for User-Update-Profile

class UserEditProfileAPIView(generics.GenericAPIView):
  """
  REST API making a PUT request for updating the details of a User. 
  """

  serializer_class       = UserEditSerializer
  authentication_classes = (TokenAuthentication,) 
  permission_classes     = [IsAuthenticated,]

  def get(self, request, *args, **kwargs):
     
    user = UserEditSerializer(request.user)
    return Response(user.data)
      

  def put(self,request,*args,**kwargs):

    if request.user.is_authenticated:
        user_id    = request.user
        serializer = UserEditSerializer(user_id, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        raise ValidationError({'status':'failed',
                               'message':'Entered Fields are not valid. Please enter correct values & try again.',
                               'data':[]}) 


    else:
      raise ValidationError({'status':'failed',
                             'message':'Invalid Login Crendtials',
                             'data':[]})      



#Api for User-Profile-Delete

class UserDeleteAPIView(generics.GenericAPIView):
  """
  REST API making a POST request for deleting the profile of a User. 
  """ 
  
  authentication_classes = [TokenAuthentication,]
  permission_classes = [IsAuthenticated,]

  def post(self,request):
    
    if request.user.is_authenticated:
      request.user.auth_token.delete()
      request.user.delete()                 
      return Response({'status':'success',
                        'message':'Account Successfully Deleted'},status=status.HTTP_200_OK)
    
    else:
       raise ValidationError({'status':'failed',
                              'message':'Invalid Login Crendtials',
                              'data':[]})  
