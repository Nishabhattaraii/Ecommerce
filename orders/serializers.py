from urllib import request
from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem

class CartItemSerializer(serializers.ModelSerializer):
    # discounted_price = serializers.SerializerMethodField()
    # total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = '__all__'
        # fields = ['product', 'quantity', 'total_price', 'discounted_price']


    # def get_total_price(self, obj):
    #     return obj.quantity * obj.product.discounted_price

    # def get_discounted_price(self, obj):
    #     return obj.product.discounted_price
    
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

    
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
