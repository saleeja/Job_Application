from django.shortcuts import render
from django.contrib.auth.models import User
from Recruiter.models import JobListing
from JobSeeker.models import CustomUser




def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})


def moderate_listings(request):
    listings = JobListing.objects.all()
    return render(request, 'admin/moderate_listings.html', {'listings': listings})


































































from .models import UserActivityLog
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# @login_required
# def admin_main(request):
#     # Fetch recent log entries
#     recent_logs = UserActivityLog.objects.filter(timestamp__gte=timezone.now() - timezone.timedelta(days=7))
    
#     context = {
#         'recent_logs': recent_logs
#     }
#     return render(request, 'admin/main_admin.html', context)















