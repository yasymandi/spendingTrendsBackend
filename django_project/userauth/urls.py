from django.urls import path
from .views import CustomTokenObtainPairView, signup

urlpatterns = [
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/signup/', signup, name='signup'),
]
