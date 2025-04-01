import uuid

from django.db import models
from account.models import User
from portal.models.skill_model import Skill
from django.core.validators import FileExtensionValidator


class JobSeekerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="job_seeker_profile")
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name="job_seekers", blank=True)
    resume = models.FileField(upload_to="resumes/",
                              validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])], blank=True,
                              null=True)

    def __str__(self):
        return self.user.username
