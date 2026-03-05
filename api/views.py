from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

class AnalyzeCV(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # קבלת הקובץ והלינק מה-Frontend
        cv_file = request.FILES.get('file')
        job_url = request.data.get('url')
        
        # כאן תבוא לוגיקת ה-NLP שלך
        # למשל: extracted_text = extract_from_pdf(cv_file)
        
        return Response({
            "message": "File received!",
            "skills": ["Python", "Django", "NLP"], # דוגמה למידע שיוחזר
        })