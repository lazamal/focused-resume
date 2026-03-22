from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator

def validate_file_size(value):
    filesize = value.size
    

    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    return value

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=300)
    alt_name = models.CharField(max_length=300)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Resume_Submission(models.Model):
    date = models.DateField(auto_now_add=True)
    file = models.FileField(
            upload_to="resumes/", 
            validators=[
                validate_file_size, 
                FileExtensionValidator(allowed_extensions=['pdf'])
            ],
            help_text="Maximum file size allowed is 5MB. Only PDF."
        )
    resume_content = models.TextField()
    job_url = models.URLField(max_length=500, blank=True, null = True)
    job_content = models.TextField(blank=True, null=True)
    job_skills = models.JSONField(default=list, blank=True)
    count_job_skills =  models.PositiveIntegerField(default=0)
    cv_skills = models.JSONField(default=list, blank=True)
    matched_skills = models.JSONField(default=list, blank=True)
    count_match_skills = models.PositiveIntegerField(default=0)
    skills_to_learn = models.JSONField(default=list, blank=True)
    count_skills_to_learn = models.PositiveIntegerField(default=0)
    overall_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage score from 0 to 100"
)
    def save(self, *args, **kwargs):
        """
        Overriding save to ensure counters and scores stay 
        synced with the list data automatically.
        """
        # Update Counters
        self.count_job_skills = len(self.job_skills)
        self.count_match_skills = len(self.matched_skills)
        self.count_skills_to_learn = len(self.skills_to_learn)

        # Calculate Percentage Score
        if self.count_job_skills > 0:
            percentage = (self.count_match_skills / self.count_job_skills) * 100
            self.overall_score = round(percentage, 2)
        else:
            self.overall_score = 0.00

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Submission {self.id} - Score: {self.overall_score}%"
    
