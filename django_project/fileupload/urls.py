from django.urls import path
from .views import upload_files, get_uploaded_files, delete_uploaded_file

urlpatterns = [
    path('api/upload-files/', upload_files, name='upload_files'),
    path('api/get-uploaded-files/', get_uploaded_files, name='get_uploaded_files'),
    path('api/delete-uploaded-file/', delete_uploaded_file, name='delete_uploaded_file'),
]
