from rest_framework import serializers
from portal.models.job_model import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('id', 'posted_at', 'is_active')
