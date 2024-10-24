from rest_framework import serializers
from .models import Order, Product, Store

class DashboardSerializer(serializers.Serializer):
    orders_placed = serializers.IntegerField()
    top_selling_products = serializers.ListField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    store_with_most_sales = serializers.CharField()
    total_products_added_to_cart = serializers.IntegerField()
