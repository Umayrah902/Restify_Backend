from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.contenttypes.models import ContentType

from .models import Booking
from notifications.models import notifications
from .serializer import BookingSerializer
# Create your views here.
class BookingsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        if booking.property_booking.owner != self.request.user and booking.client != self.request.user:
            return Response(status=HTTP_401_UNAUTHORIZED)
        if booking:
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)


class BookingEditView(APIView):
    def post(self, request, pk):
        currbooking = Booking.objects.get(pk=pk)
        if currbooking.property_booking.owner != self.request.user and currbooking.client != self.request.user:
            return Response(status=HTTP_401_UNAUTHORIZED)
        try:
            start_date = request.data['start_date']
            end_date = request.data['end_date']
            billing_address_string = request.data['billing_address_string']
            billing_address_city = request.data['billing_address_city']
            billing_address_country = request.data['billing_address_country']
            billing_address_province = request.data['billing_address_province']
            billing_address_postal_code = request.data['billing_address_postal_code']
            invoice_cost = request.data['invoice_cost']
            state = request.data['state']
            # print(dict(Booking.STATES_OPTIONS))
            # print(state not in dict(Booking.STATES_OPTIONS))

            if state not in dict(Booking.STATES_OPTIONS):
                return Response("Bad State", status=HTTP_400_BAD_REQUEST)

            currbooking.start_date = start_date
            currbooking.end_date = end_date
            currbooking.billing_address_string = billing_address_string
            currbooking.billing_address_city = billing_address_city
            currbooking.billing_address_country = billing_address_country
            currbooking.billing_address_province = billing_address_province
            currbooking.billing_address_postal_code = billing_address_postal_code
            currbooking.invoice_cost = invoice_cost
            currbooking.state = state
            currbooking.save()

            booking_ct = ContentType.objects.get_for_model(Booking)

            user_notif = notifications.objects.create(
                recipient=currbooking.client,
                details=f"The state of booking No.{currbooking.pk} has changed: {currbooking.state}.",
                notification_type=booking_ct,
                notification_id=currbooking.pk
            )

            serializer = BookingSerializer(currbooking)
            return Response(serializer.data, status=HTTP_200_OK)

        except KeyError:
            return Response("Missing Fields in Request", status=HTTP_400_BAD_REQUEST)


"""
"""
class BookingContactInfoView(APIView):
    def get(self, request):
        return None

    def post(self, request):
        return None


class BookingChangeView(APIView):
    def post(self, request):
        return None

