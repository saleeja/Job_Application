import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,JoobseekerProfile,CompanyProfile,JobApplication
from django.contrib.auth import password_validation

def validate_email(value):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, value):
        raise forms.ValidationError("Invalid email format")

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField(validators=[validate_email])
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password_validation.validate_password(password1)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'password1', 'password2', 'user_type']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = JoobseekerProfile
        fields =  ['phone_number', 'address', 'current_location', 'gender', 'experience_status', 'resume', 'profile_summary', 'key_skills', 'projects', 'education', 'certificate', 'certification_details', 'department', 'languages_known']


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'description', 'location', 'industry', 'website', 'logo']


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [ 'resume', 'cover_letter']

class JobSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Jobs', max_length=100)


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='Enter OTP', max_length=6)
