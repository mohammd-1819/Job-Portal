import uuid
from django.db import models
from portal.models.job_model import Job
from portal.models.job_seeker_profile_model import JobSeekerProfile


class JobApplication(models.Model):
    APPLICATION_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="applications/resumes/", blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=APPLICATION_STATUS, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.user.username} - {self.job.title}"
