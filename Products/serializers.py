from rest_framework import serializers
from Products.models import Product, Comment

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Product
        fields = [
            "name",
            "image",
            "description",
            "price",
            "stock",
            "discount"
        ]
    
    def create(self, validated_data):
        user = self.context.get("user")
        seller = user.seller_user
        validated_data["seller"] = seller
        
        return Product.objects.create(**validated_data)


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
