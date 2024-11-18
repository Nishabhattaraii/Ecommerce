from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from authentication.models import Seller
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerRegisterSerializer, PasswordChangeSerializer, PasswordResetConfirmSerializer, SellerRegisterSerializer, StoreSerializer
from .serializers import get_tokens_for_user
from authentication.serializers import PasswordResetRequestSerializer,LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from authentication.tasks import send_password_reset_email
from authentication.models import User
from django.conf import settings




class CustomerRegisterView(APIView):
    serializer_class =CustomerRegisterSerializer

    @extend_schema(
            request=CustomerRegisterSerializer,
            description="Customer_register"
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SellerRegisterView(APIView):
    serializer_class =SellerRegisterSerializer

    @extend_schema(
            request=SellerRegisterSerializer,
            description="Seller_register"
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Seller registered successfully"}, status=status.HTTP_201_CREATED)


class StoreRegisterView(APIView):
    serializer_class=StoreSerializer
    @extend_schema(
            request=StoreSerializer,
            description="Store_register"
    )
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    serializer_class = LoginSerializer
    @extend_schema( 
        request=LoginSerializer,
        description="Login with email and password",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, email=email, password=password)
            if user is None:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            tokens = get_tokens_for_user(user)
            return Response({
                'email': email,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        

class PasswordResetRequestView(APIView):
    serializer_class =PasswordResetRequestSerializer

    @extend_schema(
        request=PasswordResetRequestSerializer,
        description="Request a password reset link. Sends an email with the reset link if the email exists.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.FRONTEND_URL}/password-reset-confirm/{uid}/{token}/"
            
            # Enqueuing the email-sending task to Celery
            send_password_reset_email(email, reset_link)
            
            return Response({"message": "Password reset link sent!"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
class PasswordResetConfirmView(APIView):
    serializer_class =PasswordResetConfirmSerializer

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        description="Confirm password reset with new password and token.",)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class =PasswordChangeSerializer
    @extend_schema(
        request=PasswordChangeSerializer,
        description="Change the user's password after verifying the old password.",
    )
   
    def post(self, request):
        serializer =self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)