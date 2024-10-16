from django.urls import path
from .views import CustomTokenObtainPairView, signup, check_token_valid

urlpatterns = [
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/signup/', signup, name='signup'),
    path('api/check_token_valid/', check_token_valid, name='check_token_valid'),
]