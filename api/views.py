from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from playwright.sync_api import sync_playwright
import trafilatura
import fitz  # PyMuPDF
import os
from pathlib import Path


def scrape_frontend(url):
    with sync_playwright() as p:
       
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
    
        page.goto(url, wait_until="networkidle")
        

        rendered_content = page.content()
        browser.close()
        text_scraped = trafilatura.extract(rendered_content)
        return text_scraped
    


def extract_pdf(cv_file):
    # Read the uploaded file into memory
    file_content = cv_file.read()
    doc = fitz.open(stream=file_content, filetype="pdf")
    
    sidebar_text = []
    main_content_text = []

    for page in doc:
        # Get text blocks with coordinates
        blocks = page.get_text("blocks")
        
        # Sort blocks by vertical position (Y)
        blocks.sort(key=lambda b: b[1])

        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            
            # Filter out images and empty strings
            clean_text = text.strip()
            if block_type == 0 and clean_text:
                # If the block starts on the left side of the page (e.g., x < 200)
                if x0 < 200:
                    sidebar_text.append(clean_text)
                else:
                    main_content_text.append(clean_text)

    doc.close()
    
    # Combine them logically: Header/Sidebar first, then Experience
    full_cv_text = {
        "sidebar": "\n".join(sidebar_text),
        "main": "\n".join(main_content_text)
    }
    full_organized_text = full_cv_text['sidebar'] + full_cv_text['main']
    return full_organized_text
                    

@method_decorator(csrf_exempt, name='dispatch')
class AnalyzeCV(View):

    def post(self, request):
        # קבלת הקובץ והלינק מה-Frontend
        cv_file = request.FILES.get('file')
        job_url = request.POST.get('url')
        
        if not cv_file:
            return JsonResponse({"error": "No file was uploaded"}, status=400)
     
        job_text_scraped = scrape_frontend(job_url)

        pdf_text = extract_pdf(cv_file)

        with open("api/experiments/job_description.txt", 'w',encoding="utf-8" ) as f:
            f.write(job_text_scraped if job_text_scraped else "No text was scraped")

        with open("api/experiments/pdf_text.txt", 'w',encoding="utf-8" ) as f:
            f.write(pdf_text if pdf_text else "No pdf text was extacted")

        
        return JsonResponse({
            "message": f'File received! {job_text_scraped}',
            "skills": ["Python", "Django", "NLP"],
            "filename": cv_file.name,
            "url_received": job_url
        })

# to do: if the linkding url is from copy paste like this
# https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4377845628
# then convert it to this url
# https://www.linkedin.com/jobs/view/4377845628
# to make sure the job description text is being scraped currectly

def index(request):
    return HttpResponse("Hello, world. You're at the API index.")