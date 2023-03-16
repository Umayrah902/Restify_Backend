from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializer import NotificationSerializer, ReadNotificationSerializer
from .models import notifications
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

class NotificationPagination(PageNumberPagination):
    page_size = 5

#view for viewing notifications
class MyNotificationsView(ListAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination

    def get_queryset(self):
        try:
              notification_object = notifications.objects.filter(read=True)
        except notifications.DoesNotExist:
              return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
              notification_object.delete()
        
        return notifications.objects.filter(recipient=self.request.user, read=False)

#view for reading notifications
class ReadNotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReadNotificationSerializer

    def get(self, request, n):
        notifs = notifications.objects.filter(recipient=self.request.user)
        notif_id_set = set()
        for notif in notifs:
            notif_id_set.add(notif.id)
        if n in notif_id_set:
            notification_object = notifications.objects.get(id=n)
            notification_object.read = True
            notification_object.save()
            return Response(self.serializer_class(notification_object).data)
        else:
            return Response({'error': 'Invalid notification index'}, status=status.HTTP_404_NOT_FOUND)





