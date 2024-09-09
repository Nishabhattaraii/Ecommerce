from django.contrib.auth.models import User
from authentication.models import Profile
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
import re


class RegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=Profile.USER_TYPE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'user_type')

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user, user_type=user_type)
        return user
    
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }