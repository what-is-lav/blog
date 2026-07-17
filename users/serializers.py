from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return value

class UserConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)