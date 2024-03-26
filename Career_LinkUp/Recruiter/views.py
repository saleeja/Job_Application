from django.shortcuts import render, redirect, get_object_or_404
from .models import JobListing
from .forms import JobForm
from django.contrib import messages
from JobSeeker.models import CompanyProfile,JobApplication
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
@login_required
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

@login_required
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

@login_required
def delete_job(request, job_id):
    job = JobListing.objects.get(id=job_id)
    job.delete()
    return redirect('joblist_com')  


@login_required
def job_list_com(request):
    company = request.user.companyprofile
    jobs = JobListing.objects.filter(company=company)
    return render(request, 'Recruiter/job_list.html', {'jobs': jobs})



def main_comp(request):
    return render (request,'Recruiter/main.html')


# def update_application_status(request, application_id):
#     if request.method == 'POST':
#         application = JobApplication.objects.get(id=application_id)
#         new_status = request.POST.get('status')
#         application.status = new_status
#         application.save()
#     return redirect('view_all_applicants')

# def update_application_status(request, application_id):
#     if request.method == 'POST':
#         application = JobApplication.objects.get(id=application_id)
#         new_status = request.POST.get('status')
#         application.status = new_status
#         application.applicant = request.user  
#         application.applicant_email = request.user.email 
#         application.save()

#         # Send email based on status
#         subject = f'Application Status Updated: {application.job.title}'
#         message = f'Your application status for job "{application.job.title}" has been updated to "{new_status}".'
#         recipient_email = application.user.email
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email], fail_silently=False)

#     return redirect('view_all_applicants')

@login_required
def view_all_applicants(request):
    company = request.user.companyprofile
    job_applications = JobApplication.objects.filter(job__company=company).order_by('-date_applied')
    return render(request, 'Recruiter/all_applicants.html', {'job_applications': job_applications})

@login_required
def serve_resume(request, resume_path):
    resume_file_path = os.path.join(settings.MEDIA_ROOT, resume_path)
    
    if os.path.exists(resume_file_path):
        return FileResponse(open(resume_file_path, 'rb'), content_type='application/pdf')
    else:
        raise Http404("Resume not found")

@login_required
def update_application_status(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication, id=application_id)
        new_status = request.POST.get('status')
        
        if application.status != new_status: 
            old_status = application.status
            application.status = new_status
            application.save()
            
            # Send message based on status change
            subject = f'Status of your job application has changed !'
            message = f'Your application status for job {application.job.title} has been updated from {old_status} to "{new_status}".'
            recipient_email = application.applicant_email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email], fail_silently=False)

    return redirect('view_all_applicants')











