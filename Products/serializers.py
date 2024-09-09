from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # def validate(self, attrs):
    #     if not user.role == enums.Class.field :
    #         PermissionError

    #     return attrs