from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import BookingSerializer
# Create your views here.
class BookingsDetailView(APIView):
    def get(self, request):
        return None


class BookingEditView(APIView):
    def post(self, request):
        return None


class BookingContactInfoView(APIView):
    def get(self, request):
        return None

    def post(self, request):
        return None


class BookingChangeView(APIView):
    def post(self, request):
        return None

