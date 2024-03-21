from django.contrib.auth.models import AbstractUser,Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    JOB_SEEKER = 'job_seeker'
    RECRUITER = 'recruiter'
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer/Recruiter'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='job_seeker')
    full_name = models.CharField(max_length=150)
    

    def __str__(self):
        return self.username
    
    def is_job_seeker(self):
        return self.user_type == self.JOB_SEEKER

    def is_recruiter(self):
        return self.user_type == self.RECRUITER
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    # Provide unique related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name=('user permissions'), blank=True, related_name='customuser_set')
 


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    current_location = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    FRESHER = 'F'
    EXPERIENCED = 'E'
    EXPERIENCE_CHOICES = [
        (FRESHER, 'Fresher'),
        (EXPERIENCED, 'Experienced'),
    ]
    experience_status = models.CharField(max_length=1, choices=EXPERIENCE_CHOICES)
    resume = models.FileField(upload_to='resumes/')
    profile_summary = models.TextField()
    key_skills = models.CharField(max_length=255)
    projects = models.TextField()
    education = models.TextField()
    certificate = models.FileField(upload_to='certificates/')
    certification_details = models.TextField()
    department = models.CharField(max_length=100)
    languages_known = models.CharField(max_length=255)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username