from django.urls import path
from authentication import views
from authentication.views import CustomerRegisterView, LoginView, LogoutView,SellerRegisterView, StoreRegisterView
from authentication.views import PasswordChangeView,PasswordResetRequestView,PasswordResetConfirmView
urlpatterns = [
    path('', LoginView.as_view(),name = 'login'),
    path('register/',CustomerRegisterView.as_view(), name = 'customer_register'),
    path('register/seller/',SellerRegisterView.as_view(), name = 'seller_register'),
    path('register/store/',StoreRegisterView.as_view(), name = 'store_register'),
    path('logout/',LogoutView.as_view(), name = 'logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
]
