from django.shortcuts import render, redirect, get_object_or_404
from .models import JobListing
from .forms import JobForm
from django.contrib import messages


def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job successfully created!')
            return redirect('main_comp')  
    else:
        form = JobForm()
    return render(request, 'Recruiter/create_job.html', {'form': form})


def edit_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Redirect to job listing page
    else:
        form = JobForm(instance=job)
    return render(request, 'Recruiter/edit_job.html', {'form': form, 'job': job})

def delete_job(request, job_id):
    job = JobListing.objects.get(id=job_id)
    job.delete()
    return redirect('job_list')  # Redirect to job listing page

def job_list_com(request):
    jobs = JobListing.objects.all()
    return render(request, 'Recruiter/job_list.html', {'jobs': jobs})


def main_comp(request):
    return render (request,'Recruiter/main.html')





