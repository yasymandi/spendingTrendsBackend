from django.urls import path
from .views import upload_files

urlpatterns = [
    path('api/upload-files/', upload_files, name='upload_files'),
]

