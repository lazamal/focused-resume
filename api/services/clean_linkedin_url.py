import re

# to do: if the linkding url is from copy paste like this
# https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4377845628
# then convert it to this url
# https://www.linkedin.com/jobs/view/4377845628
# to make sure the job description text is being scraped currectly

def clean_linkedin_url(url):

    match = re.search(r'currentJobId=(\d+)', url)
    if match:
        job_id = match.group(1)
        return f"https://www.linkedin.com/jobs/view/{job_id}"
    return url
