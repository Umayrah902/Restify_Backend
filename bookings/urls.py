from django.urls import path
from .views import *

app_name = "bookings"
urlpatterns = [
    path('', BookingsView.as_view(), name='bookings_view'),
    path('<int:pk>/', BookingsDetailView.as_view(), name='bookings_detail_view'),
    path('<int:pk>/edit/', BookingEditView.as_view(), name='property_detail_view'),
    # path('<int:pk>/aux/', BookingContactInfoView.as_view(), name='booking_contact_view'),
    # path('<int:pk>/change/', BookingChangeView.as_view(), name='booking_change_view'),
]