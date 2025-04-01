from rest_framework import serializers
from portal.models.skill_model import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name',)
        read_only_fields = ('id',)
