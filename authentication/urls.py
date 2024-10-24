from django.urls import path
from authentication import views
from authentication.views import CustomerRegisterView, LoginView, LogoutView,SellerRegisterView, StoreRegisterView

urlpatterns = [
    path('', LoginView.as_view(),name = 'login'),
    path('register/',CustomerRegisterView.as_view(), name = 'customer_register'),
    path('register/seller/',SellerRegisterView.as_view(), name = 'seller_register'),
    path('register/store/',StoreRegisterView.as_view(), name = 'store_register'),
    path('logout/',LogoutView.as_view(), name = 'logout'),
]
