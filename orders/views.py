from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from orders.models import Cart, Order,CartItem,OrderItem
from orders.serializers import CartSerializer, OrderSerializer, CartItemSerializer
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
            request=CartSerializer,
            description="cart",
            responses=CartItemSerializer(many=True) 
    )

    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CartPostView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    @extend_schema(
            request=CartItemSerializer,
            description='add items to cart',
            responses=CartItemSerializer
    )
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

   

    @extend_schema(
            request=CartItemSerializer,
            description="update an existing item in cart",
            responses=CartItemSerializer
    )
    def put(self, request, id):
        cart = request.user.cart_user
        cart_item = CartItem.objects.filter(
            cart = cart,
            product__id = id
        ).first()
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Updated Successfully", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
            description="Remove an existing cart Item",
            responses=None
    )
    def delete(self, request, id):
        cart = request.user.cart_user
        cart_item = CartItem.objects.filter(
            cart = cart,
            product__id = id
        ).first()
        cart_item.delete()
        return Response(status=status.HTTP_200_OK)


class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description='Create order from cart',
        responses=OrderSerializer
    )
    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)

        for item in cart.items.all():
            product = item.product
            if product.stock < item.quantity:
                return Response({"error": f"Not enough stock for {product.name}."}, status=status.HTTP_400_BAD_REQUEST)
            
            product.stock -= item.quantity
            product.save()
            OrderItem.objects.create(order=order, product=product, quantity=item.quantity)

        cart.items.all().delete() 
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Update order status",
        request=OrderSerializer,
        responses=OrderSerializer
    )
    def patch(self, request, id):
        order = get_object_or_404(Order, id=id, user=request.user)
        if request.user != order.user and not request.user.is_staff:
            return Response({"error": "You do not have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)
        
        status = request.data.get('status')
        if status not in dict(Order.ORDER_STATUS_CHOICES):
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = status
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
