from django import forms
from .models import IssueReport

class IssueReportForm(forms.ModelForm):
    class Meta:
        model = IssueReport
        fields = ['issue_type', 'description']
