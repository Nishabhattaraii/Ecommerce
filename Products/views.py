from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from authentication.permissions import IsSellerUser
from .models import Product
from .serializers import ProductSerializer
from drf_spectacular.utils import extend_schema


class ProductListView(APIView):
    @extend_schema(
        request=ProductSerializer,
        description="product"
    )

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProductCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsSellerUser]
    @extend_schema(
            request=ProductSerializer,
            description="Product"
    )

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk):
       product = Product.objects.get(pk=pk)
       serializer = ProductSerializer(product,data =request.data,partial=True)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_200_OK)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    