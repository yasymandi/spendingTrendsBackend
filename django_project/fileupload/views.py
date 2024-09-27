from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def upload_file(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file part'}, status=400)
    
    file = request.FILES['file']
    return JsonResponse({'message': 'File uploaded successfully'})
