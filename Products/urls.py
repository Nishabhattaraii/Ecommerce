from django.urls import path
from Products.views import ProductListView, ProductCreateView,CommentCreateAPIView,ProductChangeView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('add/', ProductCreateView.as_view(), name='product_add'),
    path('change/<int:pk>/',ProductChangeView.as_view(),name='product_add'),
    path('comment/',CommentCreateAPIView.as_view(), name='comment')
]
