from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from playwright.sync_api import sync_playwright
import trafilatura
import fitz  # PyMuPDF
import os
from pathlib import Path
from api.services.analyze_text import Analyze_Text
from api.services.analyze_gliner import Analyze_Gliner
from api.services.compare_cv_to_job import compare_cv_to_job
from api.services.skill_blacklist import skill_blacklist
from api.services.clean_linkedin_url import clean_linkedin_url


analyzer = Analyze_Text()
# gliner_analyzer = Analyze_Gliner()

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
    def __init__(self):
        self.job_blacklist = ['tango']
    

    def post(self, request):
        # קבלת הקובץ והלינק מה-Frontend
        job_text_scraped = None
        cv_file = request.FILES.get('file')
        job_url = request.POST.get('url')
        text_description = request.POST.get('textarea')
        

        if not cv_file:
            return JsonResponse({"error": "No file was uploaded"}, status=400)
        if job_url:
            job_url = clean_linkedin_url(job_url)
            job_text_scraped = scrape_frontend(job_url)
            with open("api/experiments/job_description.txt", 'w',encoding="utf-8" ) as f:
                f.write(job_text_scraped if job_text_scraped else "No text was scraped")
            job_skills = analyzer.extract_skills_new_model(job_text_scraped)
        elif text_description:
            job_skills = analyzer.extract_skills_new_model(text_description)
        else:
            return JsonResponse({"error": "No job description uploaded"}, status=400)
        
        job_clean_blacklist = skill_blacklist(job_skills, self.job_blacklist)

        pdf_text = extract_pdf(cv_file)
 
        with open("api/experiments/pdf_text.txt", 'w',encoding="utf-8" ) as f:
            f.write(pdf_text if pdf_text else "No pdf text was extacted")
        cv_skills =  analyzer.extract_skills_new_model(pdf_text)


        matched_skills, skills_to_learn = compare_cv_to_job(job_clean_blacklist, cv_skills)
        
        count_matched_skills = len(matched_skills)
        count_skills_to_learn = len(skills_to_learn)
        overall_score = count_matched_skills / len(job_clean_blacklist)
        overall_score = str(int(overall_score*100)) + '%'
        content = job_text_scraped or text_description or "No description provided"

        return JsonResponse({
            "message": f'File received! {content}',
            'matched_skills': matched_skills,
            'skills_to_learn': skills_to_learn,
            'number_of_matched_skills': count_matched_skills,
            'number_of_skills_to_learn': count_skills_to_learn,
            'overall_score': overall_score,
            'total_skills_for_job': len(job_clean_blacklist)

        })



def index(request):
    return HttpResponse("Hello, world. You're at the API index.")