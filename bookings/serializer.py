from .models import Booking
from rest_framework import serializers


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('a', 'b')

    def create(self, validated_data):
        booking = Booking.objects.create()
        return booking
