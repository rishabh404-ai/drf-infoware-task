from django.urls import path,include
from myapp.views import (UserRegisterAPIView,
                         UserLoginAPIView,
                         UserLogoutView,
                         UserDetailsAPIView,
                         UserDeleteAPIView,
                         UserEditProfileAPIView)

urlpatterns = [    
    path('register/',UserRegisterAPIView.as_view(),name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('view-profile/', UserDetailsAPIView.as_view(), name='profile'),
    path('delete-profile/', UserDeleteAPIView.as_view(),name='delete'),
    path('update-profile/',UserEditProfileAPIView.as_view(),name='update-profile')

]  
