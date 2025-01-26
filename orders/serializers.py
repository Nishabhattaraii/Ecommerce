from urllib import request
from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from rest_framework.exceptions import ValidationError


class CartItemSerializer(serializers.ModelSerializer):
    item_price = serializers.SerializerMethodField()
    # total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        # fields = ["quantity"]
        fields = ['product', 'quantity','item_price']

    def get_item_price(self, obj):
        """Return the discounted price of the CartItem"""
        return obj.item_price()
    
    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if not product:
            raise ValidationError("Product does not exist.")

        if product.stock < quantity:
            raise ValidationError(f"Not enough stock available. Only {product.stock} items left.")

        return data
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
        # fields = [ 'product', 'quantity']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if not product:
            raise ValidationError("Product does not exist.")
        if product.stock < quantity:
            raise ValidationError(f"Not enough stock available. Only {product.stock} items left.")
        return data

    
# class OrderSerializer(serializers.ModelSerializer):
#     order_items = OrderItemSerializer(many=True, read_only=True)
#     class Meta:
#         model = Order
#         fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'order_items', 'total_amount']
        read_only_fields = ['user', 'total_amount']
