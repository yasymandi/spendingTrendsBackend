from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import CustomTokenObtainPairView, signup

urlpatterns = [
    path('api/login/', CustomTokenObtainPairView, name='token_obtain_pair'),
    path('api/signup/', signup, name='signup'),
]
