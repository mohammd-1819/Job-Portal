import uuid
from django.db import models
from portal.models.job_owner_model import JobOwner


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    owner = models.OneToOneField(JobOwner, on_delete=models.CASCADE, related_name="company")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'
