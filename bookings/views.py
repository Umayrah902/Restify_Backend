from django.db.models import Q
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.contenttypes.models import ContentType

from .models import Booking
from notifications.models import notifications
from .serializer import BookingSerializer
# Create your views here.

class BookingPagination(PageNumberPagination):
    page_size = 5

class BookingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    pagination_class = BookingPagination
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter, ]
    filterset_fields = ['state']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryfrom = self.request.query_params.get('type')
        queryset = Booking.objects.filter(Q(property_booking__owner=self.request.user) | Q(client=self.request.user))
        # assert queryfrom in ['host', 'guest', 'all']
        if queryfrom == 'host':
            queryset = Booking.objects.filter(property_booking__owner=self.request.user)
        elif queryfrom == 'guest':
            queryset = Booking.objects.filter(client=self.request.user)
        return queryset

class BookingsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            if booking.property_booking.owner != self.request.user and booking.client != self.request.user:
                return Response(status=HTTP_401_UNAUTHORIZED)
            if booking:
                serializer = BookingSerializer(booking)
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                return Response(status=HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)


class BookingEditView(APIView):
    def put(self, request, pk):
        try:
            currbooking = Booking.objects.get(pk=pk)
            if currbooking.property_booking.owner != request.user and currbooking.client != request.user:
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

                if request.user == currbooking.client:
                    if not(state == dict(Booking.STATES_OPTIONS)['RequestCancel'] or (state == "Cancelled" and currbooking.state == "Pending")):
                        return Response("A guest can only request cancellation.", status=HTTP_401_UNAUTHORIZED)

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
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)


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

