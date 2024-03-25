from django.contrib.auth.models import AbstractUser,Group, Permission
from django.db import models
from django.utils import timezone
from Recruiter.models import JobListing


class CustomUser(AbstractUser):
    JOB_SEEKER = 'job_seeker'
    RECRUITER = 'recruiter'
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer/Recruiter'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    full_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

      
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name=('user permissions'), blank=True, related_name='customuser_set')
 


class JoobseekerProfile(models.Model):
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
    

class CompanyProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)

    def __str__(self):
        return self.name


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    applicant_email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(default=timezone.now)
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.applicant.username}'s application for {self.job.title}"
    
