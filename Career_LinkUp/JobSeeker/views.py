from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm

from django.shortcuts import redirect


def index(request):
    return render(request, "index.html")

@login_required
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
    return render(request, 'JobSeeker/login.html')


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginpage') 
    else:
        form = RegistrationForm()
    return render(request, 'JobSeeker/candidate_register.html', {'form': form})


def create_profile(request):
    try:
        profile = request.user.profile  
        return redirect('main')  
    except Profile.DoesNotExist:
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
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'JobSeeker/profile_form.html', {'form': form})

def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'JobSeeker/profile_detail.html', {'profile': profile})

def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'JobSeeker/profile_edit.html', {'form': form})


def main(request):
    return render (request,'JobSeeker/main.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  
    return render(request, 'logout.html')