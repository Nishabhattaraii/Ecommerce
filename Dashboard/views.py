from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from orders.models import Order,CartItem
from Products.models import Product
from django.db.models.functions import Coalesce
from Dashboard.serializers import OutOfStockProductSerializer

class DashboardView(APIView):

    def get(self, request):
        dispatched_orders = Order.objects.count()
        
        top_selling_products = (
              Product.objects
              .annotate(total_quantity_sold=Coalesce(Sum('orderitem__quantity'), 0))  
             .order_by('-total_quantity_sold')[:5] 
             .values('name', 'total_quantity_sold')  
            )
        
        
        # Total Products Added to Cart
        total_cart_products = CartItem.objects.aggregate(total_products=Coalesce(Sum('quantity'), 0))['total_products']

        out_of_stock_items = Product.objects.filter(stock=0)
        serializer = OutOfStockProductSerializer(out_of_stock_items, many=True)
        
        data = {
            "orders_dispatched": dispatched_orders,
            "top_selling_products": list(top_selling_products),
            "total_products_added_to_cart": total_cart_products,
            "out_of_stock_items":serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)



 