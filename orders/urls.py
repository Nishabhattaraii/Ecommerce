from django.urls import path
from orders.views import CartView, OrderCreateView,CartItemView,CartPostView,OrderStatusView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cartpost/',CartPostView.as_view(),name='cart_item'),
    path('cartitem/<int:id>/', CartItemView.as_view(), name='cartitem-detail'), 
    path('order/', OrderCreateView.as_view(), name='order-create'),
    path('status/',OrderStatusView.as_view(),name='order-status')
]
