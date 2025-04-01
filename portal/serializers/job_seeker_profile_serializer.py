from rest_framework import serializers
from portal.models.job_seeker_profile_model import JobSeekerProfile


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ('id',)
