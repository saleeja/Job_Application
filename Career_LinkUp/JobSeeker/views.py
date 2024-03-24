from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import JoobseekerProfile,CompanyProfile,JobApplication
from .forms import ProfileForm,CompanyProfileForm,JobApplicationForm,RegistrationForm
from django.core.exceptions import ObjectDoesNotExist
from Recruiter.models import JobListing
from Recruiter.views import main_comp,job_list_com
import time
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from django.contrib.auth import get_user_model


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
                return redirect('profile_detail')
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


def apply_job(request, job_id):
    
    job = get_object_or_404(JobListing, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            messages.success(request, 'Application submitted successfully!')
            time.sleep(2)
            return redirect('job_list')
    else:
        form = JobApplicationForm()
    return render(request, 'JobSeeker/apply_to_job.html', {'form': form, 'job': job })
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

@login_required
def admin_main(request):
    return render(request, 'admin/admin_main.html')






