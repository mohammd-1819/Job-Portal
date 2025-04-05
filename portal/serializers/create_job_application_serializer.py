from rest_framework import serializers
from portal.models.job_application_model import JobApplication


class CreateJobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('id', 'applied_at', 'status', 'applicant')

    def validate(self, data):
        job = data.get('job')
        job_seeker = self.context.get('job_seeker')

        if job and job_seeker:
            if JobApplication.objects.filter(job=job, applicant=job_seeker).exists():
                raise serializers.ValidationError("you have already applied for this job")

        if not data.get('resume'):
            raise serializers.ValidationError("please upload your resume")

        return data
