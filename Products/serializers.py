from rest_framework import serializers
from Products.models import Product, Comment#TODO : whole path

class ProductSerializer(serializers.ModelSerializer):
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
        
        # Create and return the new Product instance
        return Product.objects.create(**validated_data)


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
