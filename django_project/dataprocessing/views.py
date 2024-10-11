from django.http import JsonResponse
import os
from django.conf import settings
from rest_framework.decorators import api_view
from fileupload.models import UploadedFile
from .models import ProcessedFile
from django.views.decorators.csrf import csrf_exempt
from .services import extract_pdf_data, extract_transactions

@csrf_exempt
@api_view(['POST'])
def process_user_files(request):
    uploaded_files = UploadedFile.objects.filter(user=request.user)
    # parse through and collect all transaction data, transform into categories 
    for file in uploaded_files:
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.url.lstrip('/')) 
        processed_file = ProcessedFile.objects.filter(file_path=file_path)
        if not processed_file.exists():
            # process the file into a corresponding ProcessedFile object
            processed_text = extract_pdf_data(file_path)
            transactions_data, categories_and_amounts = extract_transactions(processed_text)
            if not transactions_data:
                return JsonResponse({'message': 'Failed to process transactions data for ${file.file.name}'}, status=400)
            if not categories_and_amounts:
                return JsonResponse({'message': 'Failed to process categories and amounts for ${file.file.name}'}, status=400)
            processed_file = ProcessedFile.objects.create(user=request.user,
                                                          file_path=file_path,
                                                          transactions_data=transactions_data,
                                                          categories_and_amounts=categories_and_amounts)
    # collect all categories and amounts into one big dict
    all_categories_and_amounts = {}
    all_processed_files = ProcessedFile.objects.filter(user=request.user)
    for file in all_processed_files:
        categories_dict = file.categories_and_amounts
        for category in categories_dict:
            if category not in all_categories_and_amounts:
                all_categories_and_amounts[category] = 0
            all_categories_and_amounts[category] += categories_dict[category]

    return JsonResponse({'message': 'File uploaded successfully', 'data': all_categories_and_amounts}, status=200)

