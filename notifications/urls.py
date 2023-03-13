from django.urls import path
from .views import MyNotificationsView, ReadNotificationsView

app_name = "notifications"
urlpatterns = [
    path('list/', MyNotificationsView.as_view(), name='list'),
    path('list/<int:n>/', ReadNotificationsView.as_view(), name='read'),
]