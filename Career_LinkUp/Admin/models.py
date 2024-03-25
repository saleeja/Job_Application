from django.db import models
from django.utils import timezone
from JobSeeker.models import CustomUser

class UserActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"



class ReportedIssue(models.Model):
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issue_description = models.TextField()
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue reported by {self.reported_by.username}"
