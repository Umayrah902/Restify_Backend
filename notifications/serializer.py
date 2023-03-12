from rest_framework import serializers
from .models import notifications

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notifications
        fields = ['notification_id', 'details']

class ReadNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notifications
        fields = ['details']