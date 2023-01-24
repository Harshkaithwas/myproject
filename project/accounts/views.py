from django.shortcuts import render

# Create your views here.
from accounts.serializers import *
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken





def home(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def signin(request):
    return render(request, 'signin.html')


class RegistrationView(APIView):
    serializer_class = RegistrationSerializer

    def get(self, request):
        return render(request, 'signup.html')
    

    def post(self, request, *args, **kwargs):

        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            refresh = RefreshToken.for_user(Account)
            response={
                'message':'Your Account Has Been Registerd Sucessfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token),

            }
            print(response)
            return Response(response,status=status.HTTP_201_CREATED)
    
        else:
            data = {'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}
            print(data)
            
        return Response(data)


class SingInView(APIView):

    def get(self, request):
        return render(request, 'signin.html')

    def post(self, request):
        email = request.data.get("email")
        username = request.data.get('username')
        password = request.data.get("password")
        account = Account.objects.filter(email=email)
        if account.exists():
            if (email and password) or (username and password):
                user = authenticate(email=email , password=password)
                refresh = RefreshToken.for_user(Account)
                if user:
                    response = {
                    'success' : 'True',
                    'status code' : status.HTTP_200_OK,
                    'message': 'User logged in  successfully',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                    status_code = status.HTTP_200_OK
                    return Response(response,status=status_code,)
                else:
                    response = {
                        'success' : 'False',
                        'status code' : status.HTTP_400_BAD_REQUEST,
                        'message': 'Email or password is unvalid, Please correct it and try again',
                        }
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(response,  status_code)
        else:
            response = {
                    'success' : 'False',
                    'status code' : status.HTTP_400_BAD_REQUEST,
                    'message': "This account dosen't exist, please go to signup or enter a valid details",
                    }
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status_code)
            
                
class UserDeatilsView(APIView):
    serializer_class = UserDetails

    model = serializer_class.Meta.model

    def get(self, request, pk):
        try:
            user_obj = Account.objects.get(id=pk)
            serializer = UserDetails(user_obj, context={'request': request}, many=False)
            return Response(serializer.data)
        except:
            return Response({
                'message': "Account not found", 
                'status': status.HTTP_400_BAD_REQUEST
            })
  