# import re
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.core.validators import RegexValidator
# from .models import UserProfile

# def validate_email(value):
#     regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     if not re.match(regex, value):
#         raise forms.ValidationError("Invalid email format")

# def validate_password(value):
#     regex = r'^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'
#     if not re.match(regex, value):
#         raise forms.ValidationError("Password must be at least 8 characters long and contain at least one digit")

# class RegistrationForm(UserCreationForm):
#     full_name = forms.CharField(max_length=150)
#     email = forms.EmailField(validators=[validate_email])
#     password1 = forms.CharField(
#         widget=forms.PasswordInput,
#         validators=[validate_password]
#     )
#     password2 = forms.CharField(
#         widget=forms.PasswordInput,
#         validators=[validate_password]
#     )

#     class Meta:
#         model = UserProfile
#         fields = ['full_name', 'username', 'email', 'password1', 'password2']