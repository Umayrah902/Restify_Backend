from .models import CustomUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'password', 'is_host')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_host=validated_data['is_host']
        )
        return user

