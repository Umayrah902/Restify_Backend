from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializer import NotificationSerializer, ReadNotificationSerializer
from .models import notifications
from rest_framework.response import Response

#view for viewing notifications
class MyNotificationsView(ListAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = NotificationSerializer
    def get_queryset(self):
        return notifications.objects.filter(recipient=self.request.user)

#view for reading notifications
class ReadNotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReadNotificationSerializer

    def get(self, request, n):
        notifs = notifications.objects.filter(recipient=self.request.user)
        num_notifications = len(notifs)
        if n > 0 and n <= num_notifications:
            return Response(self.serializer_class(notifs[n-1]).data)
        else:
            return Response({'error': 'Invalid notification index'}, status=400)

    #once I am done reading, I somehow want to change the status so that it is seen as read, and can therefore delete

#view for deleting notifications (after you read one)




