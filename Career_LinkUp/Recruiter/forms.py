from django import forms
from .models import JobListing
from JobSeeker.models import JobApplication


class JobForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = '__all__'

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget = forms.Select(choices=JobApplication.STATUS_CHOICES)


