from rest_framework import serializers
from portal.models.job_application_model import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('id', 'applied_at')
