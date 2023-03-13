from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser

class notifications(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    details = models.TextField(max_length=255, null=False, blank=False)
    read = models.BooleanField(default=False)

    notification_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    notification_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('notification_type', 'notification_id')

    # Use GenericForeignKey:
        # - host notified when someone rates his property (Rating), posts a comment about his property (Comment), requests approval for making a reservation or cancellation. (Booking)
        # - client notified when his reservation is approved or canceled (Booking), or when the date of his approved reservations are about to come up. (Booking) 