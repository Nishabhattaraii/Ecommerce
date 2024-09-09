from django.urls import path
from authentication import views
from authentication.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(),name = 'login'),
    path('register/',RegisterView.as_view(), name = 'register'),
    path('logout/',LogoutView.as_view(), name = 'logout'),
]
