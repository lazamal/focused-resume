from django.contrib import admin
from .models import Skill, Resume_Submission

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'alt_name', 'description']
    search_fields = ['name', 'alt_name']

@admin.register(Resume_Submission)
class ResumeSubmissionAdmin(admin.ModelAdmin):

    list_display = ['id', 'date', 'overall_score', 'count_match_skills', 'job_url']
    
  
    list_filter = ['date', 'overall_score']
    
  
    search_fields = ['job_url', 'resume_content']
    

    readonly_fields = [
        'date', 
        'count_job_skills', 
        'count_match_skills', 
        'count_skills_to_learn', 
        'overall_score'
    ]
    
  
    fieldsets = (
        ('Submission Info', {
            'fields': ('date', 'file', 'job_url')
        }),
        ('Analysis Content', {
            'fields': ('resume_content', 'job_content')
        }),
        ('Skills Data', {
            'fields': ('job_skills', 'cv_skills', 'matched_skills', 'skills_to_learn')
        }),
        ('Results & Scoring', {
            'fields': ('count_job_skills', 'count_match_skills', 'count_skills_to_learn', 'overall_score')
        }),
    )