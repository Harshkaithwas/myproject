from django.urls import path, include
from . import views
from accounts.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('', views.home,),

    path('sign_up/', views.RegistrationView.as_view(), name='registration'),
    path('sign_in/', views.SingInView.as_view(), name='login'),
    path('sign_out/', views.SignOutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('userd/<int:pk>', views.UserDeatilsView.as_view()),


]
