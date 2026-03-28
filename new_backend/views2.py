import base64
import json
from playwright.sync_api import sync_playwright
import trafilatura
import fitz  # PyMuPDF
from new_backend.analyze_text import Analyze_Text
from new_backend.compare_cv_to_job import compare_cv_to_job
from new_backend.skill_blacklist import skill_blacklist
from new_backend.clean_linkedin_url import clean_linkedin_url
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from requests_toolbelt.multipart import decoder




def scrape_frontend(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-gpu",
                    "--single-process",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-setuid-sandbox",
                ]
            )
     
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
       
            
        
            page.set_default_timeout(20000) 
            
            try:
                page.goto(url, wait_until="load")
            
                rendered_content = page.content()
         
                browser.close()
                return trafilatura.extract(rendered_content)
            except PlaywrightTimeoutError:
                browser.close()
                return "TIMEOUT_ERROR" 
    except Exception as e:
  
        return None
    


def extract_pdf(file_content):
    # Read the uploaded file into memory
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
    

    full_cv_text = {
        "sidebar": "\n".join(sidebar_text),
        "main": "\n".join(main_content_text)
    }
    full_organized_text = full_cv_text['sidebar'] + full_cv_text['main']
    return full_organized_text
                    

class AnalyzeCV():
    def __init__(self):
        self.job_blacklist = ['tango']
    

    def post(self, event):
            analyzer = Analyze_Text()

   
            content_type = event.get('headers', {}).get('content-type') or event.get('headers', {}).get('Content-Type')
            body = event.get('body', '') 

            if not body:
                return {
                    "statusCode": 400, 
                    "body": json.dumps({"error": "No body found in request."})
                }

            if event.get('isBase64Encoded'):
                body_bytes = base64.b64decode(body)
            else:
                body_bytes = body.encode('utf-8') if isinstance(body, str) else body

     
            data = {}
            try:
                multipart_data = decoder.MultipartDecoder(body_bytes, content_type)
                for part in multipart_data.parts:
                    content_disposition = part.headers.get(b'Content-Disposition', b'').decode()
                    # Extract field name (e.g., 'file', 'url', or 'textarea')
                    name = content_disposition.split('name="')[1].split('"')[0]

                    if name == "file":
                        data['file_content'] = part.content  # Raw bytes for PDF
                    else:
                        data[name] = part.text  # Text for url/textarea
            except Exception as e:
        
                return {"statusCode": 400, "body": json.dumps({"error": "Failed to parse form data"})}

            # 4. Extract variables from the parsed data
            cv_file_bytes = data.get('file_content')
            job_url = data.get('url')
            text_description = data.get('textarea')

            if not cv_file_bytes:
                return {"statusCode": 400, "body": json.dumps({"error": "No resume file uploaded"})}

            # 5. Process Job Description (Scrape or Text)
            job_text_scraped = None
            if job_url:
      
                cleaned_url = clean_linkedin_url(job_url)
                job_text_scraped = scrape_frontend(cleaned_url)
                
                if not job_text_scraped or job_text_scraped == "TIMEOUT_ERROR":
                    return {
                        "statusCode": 408,
                        "body": json.dumps({"error": "LinkedIn might be blocking us. try switching to text and paste the job description"})
                    }

        
                job_skills = analyzer.extract_skills_new_model(job_text_scraped)
            elif text_description:
        
                job_skills = analyzer.extract_skills_new_model(text_description)
            else:
                return {"statusCode": 400, "body": json.dumps({"error": "No job description provided"})}

        
            job_clean_blacklist = skill_blacklist(job_skills, self.job_blacklist)
            
            if not job_clean_blacklist:
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin": "*", 
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({
                        "overall_score": 0,
                        "matched_skills": [],
                        "skills_to_learn": [],
                        "number_of_matched_skills": 0,
                        "total_skills_for_job": 0,
                        "message": "No skills detected in job description."
                    })
    }

            
        
            pdf_text = extract_pdf(cv_file_bytes)
            cv_skills = analyzer.extract_skills_new_model(pdf_text)
            
            matched_skills, skills_to_learn = compare_cv_to_job(job_clean_blacklist, cv_skills)

            # 8. Calculate Scoring
            count_matched = len(matched_skills)
            count_to_learn = len(skills_to_learn)
            score_val = count_matched / len(job_clean_blacklist)
            overall_score = f"{int(score_val * 100)}%"

            # 9. Return Final Results
            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*" # Required for CORS
                },
                "body": json.dumps({
                    "matched_skills": matched_skills,
                    "skills_to_learn": skills_to_learn,
                    "number_of_matched_skills": count_matched,
                    "number_of_skills_to_learn": count_to_learn,
                    "overall_score": overall_score,
                    "total_skills_for_job": len(job_clean_blacklist)
                })
            }


