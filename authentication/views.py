from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from authentication.models import Seller
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerRegisterSerializer, SellerRegisterSerializer, StoreSerializer
from .serializers import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
# from authentication.views import LoginView


class CustomerRegisterView(APIView):
    @extend_schema(
            request=CustomerRegisterSerializer,
            description="Customer_register"
    )
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SellerRegisterView(APIView):
    @extend_schema(
            request=SellerRegisterSerializer,
            description="Seller_register"
    )
    def post(self, request):
        serializer = SellerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Seller registered successfully"}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreRegisterView(APIView):
    @extend_schema(
            request=StoreSerializer,
            description="Store_register"
    )
    def post(self,request):
        serializer = StoreSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    @extend_schema(
    #         request=LoginView,
    #         description="Login"
    
     request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        },
        description="Login with username and password",
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        tokens = get_tokens_for_user(user)
        return Response({
            'username': username,
            'tokens': tokens
        }, status=status.HTTP_200_OK)
            
         
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  