from .models import Booking
from rest_framework import serializers


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('pk', 'client', 'property_booking', 'billing_address_string', 'billing_address_city',
                  'billing_address_country', 'billing_address_province', 'billing_address_postal_code',
                  'start_date', 'end_date', 'invoice_cost', 'state', )

    def create(self, validated_data):
        booking = BookingSerializer(**validated_data)
        return booking

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
