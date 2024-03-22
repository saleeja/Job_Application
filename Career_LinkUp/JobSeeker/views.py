from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib import messages
from .models import JoobseekerProfile,CompanyProfile
from .forms import ProfileForm,CompanyProfileForm,ApplyJobForm
from django.urls import reverse
from Recruiter.views import main_comp,job_list_com

def index(request):
    return render(request, "index.html")

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginpage') 
    else:
        form = RegistrationForm()
    return render(request, 'JobSeeker/candidate_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email_or_username = request.POST['email_or_username']
        password1 = request.POST['password1'] 
        user = authenticate(request, username=email_or_username, password=password1)

        if user is not None:
            login(request, user)
            if user.user_type == 'job_seeker':
                return redirect('create_profile')
            elif user.user_type == 'employer':
                return redirect('create_company_profile')
            else:
                messages.error(request, 'Invalid email/username or password. Please try again.')
        messages.error(request, 'Invalid email/username or password. Please try again.')
    return render(request, 'JobSeeker/loginpage.html')


from .models import JoobseekerProfile  
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

from django.core.exceptions import ObjectDoesNotExist
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


from django.shortcuts import render
from Recruiter.models import JobListing
from django.http import JsonResponse


def job_list(request):
    job_listings = JobListing.objects.all()
    context = {
        'job_listings': job_listings
    }

    # Render the template with the context data
    return render(request, 'JobSeeker/main.html', context)  # Fetch all job listings

# views.py in the job_seeker app

from django.shortcuts import render, redirect
from .forms import JobApplicationForm

def apply_to_job(request, job_id):
    job = JobListing.objects.get(id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.job = job
            job_application.save()
            return redirect('job_list')  # Redirect to job listings page
    else:
        form = JobApplicationForm()
    return render(request, 'JobSeeker/apply_to_job.html', {'form': form, 'job': job})


from .forms import JobSearchForm

def job_search(request):
    if request.method == 'POST':
        form = JobSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # Perform job search based on search query
            job_listings = JobListing.objects.filter(title__icontains=search_query)
            return render(request, 'JobSeeker/main.html', {'job_listings': job_listings, 'search_query': search_query})
    else:
        form = JobSearchForm()
    return render(request, 'JobSeeker/main.html', {'form': form})

# views.py

from django.shortcuts import render
from .models import JobApplication

def job_application_status(request):
    # Get job applications submitted by the logged-in job seeker
    job_applications = JobApplication.objects.filter(applicant=request.user)

    return render(request, 'job_seeker/application_status.html', {'job_applications': job_applications})
