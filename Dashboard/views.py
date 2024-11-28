from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from authentication.models import Seller
from orders.models import Order, OrderItem,CartItem
from Products.models import Product
from Products.serializers import ProductSerializer
from django.db.models.functions import Coalesce, Cast
from Dashboard.serializers import OutOfStockProductSerializer

class DashboardView(APIView):

    def get(self, request):
        dispatched_orders = Order.objects.count()
        
        top_selling_products = (
              Product.objects
              .annotate(total_quantity_sold=Coalesce(Sum('orderitem__quantity'), 0))  # Use 'orderitem' based on the OrderItem model
             .order_by('-total_quantity_sold')[:5]  # Sort by the total quantity sold in descending order
             .values('name', 'total_quantity_sold')  # Select only the product name and the total quantity sold
            )
        
        
        # Total Products Added to Cart
        total_cart_products = CartItem.objects.aggregate(total_products=Coalesce(Sum('quantity'), 0))['total_products']

        out_of_stock_items = Product.objects.filter(stock=0)
        serializer = OutOfStockProductSerializer(out_of_stock_items, many=True)
        
        # Response Data
        data = {
            "orders_dispatched": dispatched_orders,
            "top_selling_products": list(top_selling_products),
            "total_products_added_to_cart": total_cart_products,
            "out_of_stock_items":serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)



 