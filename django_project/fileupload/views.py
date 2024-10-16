from django.http import JsonResponse
import os
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedFile
from dataprocessing.models import ProcessedFile

@csrf_exempt
@api_view(['POST'])
def upload_files(request):
    if 'files' not in request.FILES:
        return JsonResponse({'error': 'No file part'}, status=400)

    files = request.FILES.getlist('files')
    for file in files:
        existing_file = UploadedFile.objects.filter(user=request.user, file__icontains=file.name)
        if not existing_file and file.size > 0:
            UploadedFile.objects.create(user=request.user, file=file)
    return JsonResponse({'message': 'File uploaded successfully'})

@api_view(['GET'])
def get_uploaded_files(request):
    print(request.user)
    uploaded_files = UploadedFile.objects.filter(user=request.user)
    files_data = []
    for file in uploaded_files:
        # print(file.file.file)
        files_data.append({
            'name': file.file.name,  # This returns the path relative to MEDIA_ROOT
            'url': file.file.url      # This provides the URL to access the file
        })

    return JsonResponse(files_data, safe=False)

@api_view(['DELETE'])
def delete_uploaded_file(request):
    file_url = request.data.get('file').get('url')
    file_name = request.data.get('file').get('name')
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, file_url.lstrip('/')) 
        file_to_delete = UploadedFile.objects.filter(user=request.user, file__icontains=file_name)
        processed_file_to_delete = ProcessedFile.objects.filter(file_path=file_path)
        if processed_file_to_delete.exists():
            processed_file_to_delete.delete()
        file_to_delete.delete()
        if os.path.exists(file_path):
            os.remove(file_path)  # Delete the file from the file system

        return JsonResponse({"message": "File deleted successfully"}, status=204)  # No content
    except UploadedFile.DoesNotExist:
        return JsonResponse({"error": "File not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)