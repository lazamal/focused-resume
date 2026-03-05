from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class AnalyzeCV(View):

    def post(self, request):
        # קבלת הקובץ והלינק מה-Frontend
        cv_file = request.FILES.get('file')
        job_url = request.POST.get('url')
        
        if not cv_file:
            return JsonResponse({"error": "No file was uploaded"}, status=400)
        

        
        return JsonResponse({
            "message": "File received!",
            "skills": ["Python", "Django", "NLP"],
            "filename": cv_file.name,
            "url_received": job_url
        })



def index(request):
    return HttpResponse("Hello, world. You're at the API index.")