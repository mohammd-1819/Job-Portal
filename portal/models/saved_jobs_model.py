import uuid
from django.db import models
from portal.models.job_model import Job
from portal.models.job_seeker_profile_model import JobSeekerProfile


class SavedJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name="saved_jobs")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saved_by")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job_seeker', 'job')

    def __str__(self):
        return f"{self.job_seeker.user.username} saved {self.job.title}"
