from rest_framework import serializers
from portal.models.job_application_model import JobApplication


class JobApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('status',)
        # read_only_fields = ('id', 'applied_at', 'status', 'applicant')
