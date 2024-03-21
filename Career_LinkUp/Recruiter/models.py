# models.py

from django.db import models
from django.utils import timezone



class JobListing(models.Model):

    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_qualifications = models.TextField()
    desired_qualifications = models.TextField()
    responsibilities = models.TextField()
    application_deadline = models.DateTimeField(default=timezone.now)
    salary_range = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    company_benefits = models.TextField()
    how_to_apply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


