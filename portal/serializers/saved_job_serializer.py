from rest_framework import serializers
from portal.models.saved_jobs_model import SavedJob


class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = '__all__'
        read_only_fields = ('id', 'saved_at')
