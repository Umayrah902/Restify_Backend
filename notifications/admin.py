from django.contrib import admin

from .models import notifications

class notificationsAdmin(admin.ModelAdmin):
    fields = ['recipient', 'notification_type', 'notification_id', 'content_object']
    readonly_fields = ['content_object']
    class Meta:
        model = notifications

admin.site.register(notifications, notificationsAdmin)
