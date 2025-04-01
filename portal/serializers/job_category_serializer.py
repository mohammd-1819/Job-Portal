from rest_framework import serializers
from portal.models.job_category_model import JobCategory


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ('name',)
        read_only_fields = ('id',)
