
def compare_cv_to_job(job_array, cv_array):
    job_set = {skill.lower() for skill in job_array}
    cv_set = {skill.lower() for skill in cv_array}

    matched_skills = list(job_set & cv_set)
    skills_to_learn = list(job_set - cv_set)

    return matched_skills, skills_to_learn

    
