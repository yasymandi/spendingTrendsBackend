from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def upload_files(request):
    if 'files' not in request.FILES:
        return JsonResponse({'error': 'No file part'}, status=400)
    
    files = request.FILES.getlist('files')
    for file in files:
        pass
    return JsonResponse({'message': 'File uploaded successfully'})
