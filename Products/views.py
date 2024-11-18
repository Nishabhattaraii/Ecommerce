from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from authentication.permissions import IsSellerUser
from Products.models import Product,Comment
from rest_framework import generics
from Products.serializers import ProductSerializer,CommentModelSerializer
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema


class ProductFilter(filters.FilterSet):
    price = filters.NumberFilter()

    class Meta:
        model = Product
        fields = ['price']


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # Use both DjangoFilterBackend and OrderingFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter  # Your custom filter set class
    ordering = ['price']  # Default ordering

    @extend_schema(
        description="Retrieve a list of products with optional filtering and ordering",
        request=None, 
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class ProductCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsSellerUser]
    parser_classes = [MultiPartParser]
    serializer_class = ProductSerializer
    @extend_schema(
            request=ProductSerializer,
            description="Product"
    )
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context = {
            'user':user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class ProductChangeView(APIView):

    permission_classes = [permissions.IsAuthenticated,IsSellerUser]
    parser_classes = [MultiPartParser]
    serializer_class = ProductSerializer


    @extend_schema(
        request=ProductSerializer, 
        responses=ProductSerializer, 
        description="Update an existing product"
    )
    def put(self, request,pk):
       product = Product.objects.get(pk=pk)
       serializer = self.serializer_class(product,data =request.data,partial=True)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_200_OK)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=None, 
        responses=None, 
        description="Delete an existing product"
    )
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer