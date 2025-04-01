from rest_framework import serializers
from portal.models.job_owner_model import JobOwner


class JobOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOwner
        fields = ('user',)
        read_only_fields = ('id',)
