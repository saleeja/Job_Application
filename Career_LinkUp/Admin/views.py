from django.shortcuts import render
from django.contrib.auth.models import User
from Recruiter.models import JobListing


def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})


def moderate_listings(request):
    listings = JobListing.objects.all()
    return render(request, 'admin/moderate_listings.html', {'listings': listings})















# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry

@login_required
def admin_dashboard(request):
    # Example: Fetch recent log entries from the admin interface
    recent_logs = LogEntry.objects.order_by('-action_time')[:10]

    context = {
        'recent_logs': recent_logs,
        # Add more data to the context as needed
    }
    return render(request, 'admin_dashboard.html', context)


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            # Redirect to the admin dashboard or any other page
            return redirect('admin_dashboard')
        else:
            # Display an error message if authentication fails
            messages.error(request, 'Invalid username or password.')
    return render(request, 'admin_login.html')
