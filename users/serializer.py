from .models import CustomUser
from reviews.models import Comment
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


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name', 'phone_number', 'email')

class GuestReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('rating_num', 'comment_text', 'reviewer')
    
    def create(self, validated_data):
        review = Comment(**validated_data)
        return review

class UserSerializerProfile(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'password', 'is_host', 'avatar')

class UserSerializerPublicProfile(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'is_host', 'avatar')

