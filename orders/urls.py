from django.urls import path
from .views import CartView, OrderCreateView,CartItemView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cartitem/',CartItemView.as_view(),name='cart_item'),
    path('order/', OrderCreateView.as_view(), name='order-create'),
]
