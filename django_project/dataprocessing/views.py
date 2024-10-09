from django.http import JsonResponse
import os
from django.conf import settings
from rest_framework.decorators import api_view
from fileupload.models import UploadedFile
from .models import ProcessedFile
from django.views.decorators.csrf import csrf_exempt
from .services import extract_pdf_data

@csrf_exempt
@api_view(['POST'])
def process_user_files(request):
    uploaded_files = UploadedFile.objects.filter(user=request.user)
    processed_files = []
    for file in uploaded_files:
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.url.lstrip('/')) 
        processed_file = ProcessedFile.objects.filter(file_path=file_path)
        if not processed_file.exists():
            # process the file into a corresponding ProcessedFile object
            processed_text = extract_pdf_data(file_path)
            processed_file = ProcessedFile.objects.create(user=request.user, file_path=file_path, processed_text=processed_text)
        processed_files.append(processed_file)
    if len(processed_files) == 0:
        return JsonResponse({'message': 'Failed to process uploaded files'}, status=400)
    return JsonResponse({'message': 'File uploaded successfully'}, status=200)