from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import JoobseekerProfile,CompanyProfile,JobApplication,CustomUser
from .forms import ProfileForm,CompanyProfileForm,JobApplicationForm,RegistrationForm
from django.core.exceptions import ObjectDoesNotExist
from Recruiter.models import JobListing
from Recruiter.views import main_comp,job_list_com
from Recruiter.views import main_comp,job_list_com
from django.db.models import F
import time
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from Admin.models import UserActivityLog
from django.contrib.admin.views.decorators import staff_member_required
from Recruiter.models import JobListing
from Recruiter.forms import JobForm 
from Admin.models import IssueReport
from Admin.forms import IssueReportForm



def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False) 
                user.username = form.cleaned_data['username']  
                user.set_password(form.cleaned_data['password1'])  
                user.save()

                # Generate OTP and send email
                otp = get_random_string(length=6, allowed_chars='1234567890')
                subject = 'Email Verification OTP'
                message = f'Your OTP is: {otp}'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

                # Store OTP and email in session for verification
                request.session['otp'] = otp
                request.session['email'] = user.email

                # Redirect to verify email page
                return redirect('otp_verification')
            except IntegrityError:
                form.add_error('email', 'Email address already in use. Please try another one.')
    else:
        form = RegistrationForm()
    return render(request, 'JobSeeker/candidate_register.html', {'form': form})



def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        expected_otp = request.session.get('otp')

        if entered_otp == expected_otp:
            # OTP verification successful
            messages.success(request, 'Email verified successfully. You can now login.')
            del request.session['otp']
            return redirect('loginpage')
        else:
            # OTP verification failed
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'JobSeeker/otp_verification.html')



def index(request):
    return render(request, "index.html")


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.user_type == 'job_seeker':
                return redirect('create_profile')
            elif user.user_type == 'employer':
                return redirect('create_company_profile')
            elif user.is_superuser:
                return redirect('admin_main')
        else:
            messages.error(request, 'Invalid email/username or password. Please try again.')

    return render(request, 'JobSeeker/loginpage.html')

import logging

logger = logging.getLogger(__name__)
# profile_creation
def create_profile(request):
    try:
        profile = request.user.joobseekerprofile  
        return redirect('main_seeker')  
    except JoobseekerProfile.DoesNotExist: 
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user  
                profile.save()
                logger.info("Form saved successfully")
                return redirect('profile_detail')
            else:
                logger.error("Form errors: %s", form.errors)
                # return redirect('profile_detail')
        else:
            form = ProfileForm()
        return render(request, 'JobSeeker/profile_form.html', {'form': form})


def update_profile(request):
    profile = JoobseekerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'JobSeeker/profile_form.html', {'form': form})

def profile_detail(request):
    try:
        profile = JoobseekerProfile.objects.get(user=request.user)
        return render(request, 'JobSeeker/profile_detail.html', {'profile': profile})
    except ObjectDoesNotExist:
        return redirect('create_profile')

def edit_profile(request):
    profile = JoobseekerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'JobSeeker/profile_edit.html', {'form': form})


def main_seeker(request):
    return redirect('job_list')
    # return render (request,'JobSeeker/main.html')


def create_company_profile(request):
    try:
        profile = request.user.companyprofile  
        return redirect('main_comp')  
    except CompanyProfile.DoesNotExist:
        if request.method == 'POST':
            form = CompanyProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user  
                profile.save()
                return redirect('com_profile_detail')
        else:
            form = CompanyProfileForm()
        return render(request, 'Recruiter/create_profile.html', {'form': form})
    

def com_update_profile(request):
    try:
        profile = CompanyProfile.objects.get(user=request.user)
    except CompanyProfile.DoesNotExist:
        return redirect('com_create_profile')  
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('com_profile_detail')
    else:
        form = CompanyProfileForm(instance=profile)
    return render(request, 'Recruiter/company_profile_detail.html', {'form': form})

    
def com_profile_detail(request):
    try:
        profile = CompanyProfile.objects.get(user=request.user)
        return render(request, 'Recruiter/company_profile_detail.html', {'profile': profile})
    except CompanyProfile.DoesNotExist:
        return redirect('com_create_profile')
    
def com_edit_profile(request):
    profile = CompanyProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('com_profile_detail')
    else:
        form = CompanyProfileForm(instance=profile)
    return render(request, 'Recruiter/profile_edit.html', {'form': form})



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')  
    # return render(request, 'JobSeeker/logout.html')


def job_list(request):
    job_listings = JobListing.objects.all()
    context = {
        'job_listings': job_listings
    }

    return render(request, 'JobSeeker/main.html', context) 



def job_list_applicant(request):
    jobs = JobListing.objects.all()
    return render(request, 'JobSeeker/job_list_applicant.html', {'jobs': jobs})



# def apply_job(request, job_id):
#     job = get_object_or_404(JobListing, id=job_id)
#     already_applied = False  
    
#     if request.method == 'POST':
#         form = JobApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             if JobApplication.objects.filter(job=job, applicant=request.user).exists():
#                 messages.error(request, 'You have already applied for this job.')
#                 return redirect('job_list')
                
#             application = form.save(commit=False)
#             application.job = job
#             application.applicant = request.user  
#             application.applicant_email = request.user.email 
#             application.save()
#             messages.success(request, 'Application submitted successfully!')
#             return redirect('job_list')
#     else:
#         form = JobApplicationForm()
#         if request.user.is_authenticated:
#             already_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    
#     return render(request, 'JobSeeker/apply_to_job.html', {'form': form, 'job': job, 'already_applied': already_applied})


def main_page(request):
    return render (request,'JobSeeker/main.html')

def job_applications(request):
    applications = JobApplication.objects.all()
    return render(request, 'JobSeeker/job_applications.html', {'applications': applications})

def application_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    return render(request, 'JobSeeker/application_status.html', {'application': application})

def applied_job_list(request):
    user_applications = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'JobSeeker/job_list_applicant.html', {'user_applications': user_applications})


def job_search(request):
    query = request.GET.get('query')
    if query:
        job_listing = JobListing.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(company__name__icontains=query) |  
            Q(created_at__icontains=query) |    
            Q(job_type__icontains=query)
        )
        return render(request, 'JobSeeker/job_search_list.html', {'job_listing': job_listing, 'query': query})
    else:
        return redirect('job_list')  


# --------------------------------------------
@login_required
def admin_main(request):
   return redirect('newly_joined_users')
    

def newly_joined_users(request):
    regular_users = CustomUser.objects.filter(is_staff=False)

    admin_user = CustomUser.objects.filter(is_staff=True).first()

    if admin_user:
        regular_users = regular_users.exclude(id=admin_user.id)

    newly_joined_users = regular_users.order_by('-created_at')

    return render(request, 'admin/main_admin.html', {'newly_joined_users': newly_joined_users})



def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'admin/user_profile.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_main')
    return render(request, 'admin/delete_user.html', {'user': user})



@login_required
@staff_member_required
def admin_job_listings(request):
    # Retrieve all job listings
    all_listings = JobListing.objects.all()
    return render(request, 'admin/job_listings.html', {'job_listings': all_listings})


@login_required
@staff_member_required
def edit_job_listing(request, listing_id):
    listing = get_object_or_404(JobListing, pk=listing_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('admin_job_listings')
    else:
        form = JobForm(instance=listing)
    return render(request, 'admin/edit_job_listing.html', {'form': form, 'listing': listing})


@login_required
@staff_member_required
def delete_job_listing(request, listing_id):
    listing = get_object_or_404(JobListing, pk=listing_id)
    if request.method == 'POST':
        listing.delete()
        return redirect('admin_job_listings')
    return render(request, 'admin/delete_job_listing.html', {'listing': listing})


@login_required
@staff_member_required
def approve_job_listing(request, listing_id):
    listing = get_object_or_404(JobListing, pk=listing_id)
    listing.status = 'approved'
    listing.save()
    return redirect('admin_job_listings')


def report_issue(request):
    if request.method == 'POST':
        form = IssueReportForm(request.POST)
        if form.is_valid():
            issue_report = form.save(commit=False)
            issue_report.user = request.user
            issue_report.save()
            return redirect('issue_report_confirmation')  
    else:
        form = IssueReportForm()
    return render(request, 'JobSeeker/report_issue.html', {'form': form})


def issue_report_confirmation(request):
    return render(request, 'JobSeeker/issue_report_confirmation.html')

def admin_issue_reports(request):
    issue_reports = IssueReport.objects.all()
    return render(request, 'JobSeeker/admin_issue_reports.html', {'issue_reports': issue_reports})


def send_issue_resolved_email(user_email):
    subject = 'Your reported issue has been resolved'
    message = 'Your reported issue has been resolved. Thank you for your patience.'
    sender_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender_email, [user_email], fail_silently=False)

def update_issue_report_status(request, report_id):
    issue_report = IssueReport.objects.get(id=report_id)
    issue_report.status = 'resolved'
    issue_report.save()
    send_issue_resolved_email(issue_report.user.email)
    return redirect('admin_issue_reports')

from django.http import HttpResponse

def apply_for_job(request):
    # Process job application logic
    # Sending email
    subject = 'Job Application'
    message = 'Thank you for applying for the job.'
    from_email = 'your@example.com'  # Replace with your actual email address
    to_email = ['recipient@example.com']  # Replace with recipient's email address
    send_mail(subject, message, from_email, to_email)

    return HttpResponse('Job application submitted successfully.')


def apply_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    already_applied = False  
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            if JobApplication.objects.filter(job=job, applicant=request.user).exists():
                messages.error(request, 'You have already applied for this job.')
                return redirect('job_list')
                
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user  
            application.applicant_email = request.user.email 
            application.save()
            print(application)
            # Sending email notification to the recruiter
            subject = f"A new job application has been submitted for the position of { job.title } at your company."
            message = f"{ application.cover_letter } You can review the application details and take further action as needed."
            sender_email =  settings.EMAIL_HOST_USER  
            recipient_email = job.company.user.email  # Assuming user is a CustomUser instance linked to CompanyProfile
            send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)
            
            messages.success(request, 'Application submitted successfully! An email notification has been sent to the recruiter.')
            return redirect('job_list')
    else:
        form = JobApplicationForm()
        if request.user.is_authenticated:
            already_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    
    return render(request, 'JobSeeker/apply_to_job.html', {'form': form, 'job': job, 'already_applied': already_applied})
