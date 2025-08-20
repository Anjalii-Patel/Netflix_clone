# backend/users/urls.py
from django.urls import path
from .views import RegisterView, ProtectedView, PlanListView, SubscribeCheckoutView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('plans/', PlanListView.as_view(), name='plans'),
    path('subscribe/checkout/', SubscribeCheckoutView.as_view(), name='subscribe_checkout'),
]
