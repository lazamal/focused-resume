import re


def clean_linkedin_url(url):

    match = re.search(r'currentJobId=(\d+)', url)
    if match:
        job_id = match.group(1)
        return f"https://www.linkedin.com/jobs/view/{job_id}"
    return url
