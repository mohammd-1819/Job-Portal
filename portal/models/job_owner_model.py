import uuid
from django.db import models
from account.models import User


class JobOwner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Job_owner')

    def __str__(self):
        return self.user.username
