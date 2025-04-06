from rest_framework import serializers
from portal.models.saved_jobs_model import SavedJob


class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = '__all__'
        read_only_fields = ('id', 'job_seeker', 'saved_at')

    def validate(self, attrs):
        job = attrs.get('job')
        job_seeker = self.context['job_seeker']

        if SavedJob.objects.filter(job_seeker=job_seeker, job=job).exists():
            raise serializers.ValidationError("you have already saved this job")

        return attrs
