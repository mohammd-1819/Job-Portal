import re
from rest_framework import serializers
from account.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'fullname', 'password')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already taken')
        return value

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("invalid email address")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("password must contain 8 characters")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("password must contain both numbers and letters")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            fullname=validated_data.get('fullname', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'fullname')


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)
