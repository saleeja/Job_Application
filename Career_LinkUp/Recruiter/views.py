from django.shortcuts import render, redirect, get_object_or_404
from .models import JobListing
from .forms import JobForm
from django.contrib import messages
from JobSeeker.models import CompanyProfile,JobApplication

def create_job(request):
    companies = CompanyProfile.objects.all()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.companyprofile  
            job.save()
            messages.success(request, 'Job successfully created!')
            return redirect('main_comp')  
    else:
        form = JobForm()
    return render(request, 'Recruiter/create_job.html', {'form': form, 'companies': companies})


def edit_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('joblist_com') 
    else:
        form = JobForm(instance=job)
    return render(request, 'Recruiter/edit_job.html', {'form': form, 'job': job})


def delete_job(request, job_id):
    job = JobListing.objects.get(id=job_id)
    job.delete()
    return redirect('joblist_com')  


def job_list_com(request):
    jobs = JobListing.objects.all()
    return render(request, 'Recruiter/job_list.html', {'jobs': jobs})


def main_comp(request):
    return render (request,'Recruiter/main.html')


def view_all_applicants(request):
    job_applications = JobApplication.objects.all()
    return render(request, 'Recruiter/all_applicants.html', {'job_applications': job_applications})


def update_application_status(request, application_id):
    if request.method == 'POST':
        application = JobApplication.objects.get(id=application_id)
        new_status = request.POST.get('status')
        application.status = new_status
        application.save()
    return redirect('view_all_applicants')



from django.http import FileResponse, Http404
from django.conf import settings
import os

def serve_resume(request, resume_path):
    resume_file_path = os.path.join(settings.MEDIA_ROOT, resume_path)
    
    if os.path.exists(resume_file_path):
        return FileResponse(open(resume_file_path, 'rb'), content_type='application/pdf')
    else:
        raise Http404("Resume not found")














