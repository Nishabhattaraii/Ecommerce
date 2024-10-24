from authentication.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
import re
from .models import Customer, Seller,Store


class CustomerRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(required=True)

    class Meta:
        model = Customer
        fields = ['email', 'password','full_name', 'address', 'phone_number']

    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
    
    
    def validate_password(self, password):
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError(
                {"message": ["Password must contain at least one uppercase letter"]}
            )
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError(
                {"message": ["Password must contain at least one lowercase letter"]}
            )
        if not re.search(r"\d", password):
            raise serializers.ValidationError(
                {"message": ["Password must contain at least one number"]}
            )
        if not re.search(r"[^\w\s]", password):
            raise serializers.ValidationError(
                {"message": ["Password must contain at least one special character"]}
            )
        return password
    
    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        user = User.objects.create_user(email=email, password=password, username=email)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['name', 'address']

class SellerRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = Seller
        fields = ['email','password', 'full_name', 'store']

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists")
        return value
        

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        store = validated_data.pop('store')
        user = User.objects.create_user(email=email, password=password,username=email)
        seller = Seller.objects.create(user=user, store=store, **validated_data)
        return seller   



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }