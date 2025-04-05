from rest_framework import serializers
from portal.models.job_application_model import JobApplication
from portal.serializers.job_serializer import JobSerializer


class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer()

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('id', 'applied_at')
