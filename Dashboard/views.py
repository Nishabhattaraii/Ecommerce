from django.shortcuts import render
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, Product, Store, CartItem

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders_dispatched = Order.objects.filter(is_dispatched=True).count()

        top_selling_products = Product.objects.annotate(
            total_sold=Sum('orderitem__quantity')
        ).order_by('-total_sold')[:5] 

        #top selling product
        top_selling_products_data = [
            {'name': product.name, 'total_sold': product.total_sold} for product in top_selling_products
        ]

        total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))['total_sales']
        #store with most sales
        store_with_most_sales = Store.objects.annotate(
            total_sales=Sum('product__orderitem__quantity')
        ).order_by('-total_sales').first()

        # Total Products Added to Cart
        total_products_added_to_cart = CartItem.objects.aggregate(
            total_cart_items=Sum('quantity')
        )['total_cart_items']

        # Preparing the response data
        data = {
            'orders_dispatched': orders_dispatched,
            'top_selling_products': top_selling_products_data,
            'total_sales': total_sales,
            'store_with_most_sales': store_with_most_sales.name if store_with_most_sales else None,
            'total_products_added_to_cart': total_products_added_to_cart,
        }

        return Response(data)

