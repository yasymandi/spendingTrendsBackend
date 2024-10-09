from django.urls import path
from .views import process_user_files

urlpatterns = [
    path('api/process-user-files/', process_user_files, name='process_user_files'),
]