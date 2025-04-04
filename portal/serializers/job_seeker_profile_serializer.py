from rest_framework import serializers
from portal.models.job_seeker_profile_model import JobSeekerProfile


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ('id', 'user')

    def validate(self, data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if JobSeekerProfile.objects.filter(user=request.user).exists():
                raise serializers.ValidationError("you already have a job seeker profile")
        return data

    def validate_resume(self, value):
        max_size = 2 * 1024 * 1024
        if value and value.size > max_size:
            raise serializers.ValidationError("Your resume must be below 2mb")

        if not value:
            raise serializers.ValidationError('Please upload your resume')

        return value

    def validate_skills(self, value):
        if not value:
            raise serializers.ValidationError("حداقل یک مهارت باید انتخاب شود.")
        return value
