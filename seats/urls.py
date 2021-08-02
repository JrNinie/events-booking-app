# coding: utf-8

"""
URL Dispatcher
"""

from django.urls import path
from django.urls import include
from . import views

app_name = "seats"

urlpatterns = [
    # Base URL (all events)
    path("", views.index, name="index"),
    # Login/logout
    path("accounts/", include("django.contrib.auth.urls")),
    # Room page
    path("event/<int:event_id>/room/<int:room_id>/", views.room, name="room"),
    # Seat related URLs
    path("event/<int:event_id>/room/<int:room_id>/selection/<str:seat_ids>/", views.seat_selection, name="seat_selection"),
    # User bookings' list
    path("user/booking", views.BookingView.as_view(), name="booking"),
    # Booking delete
    path("user/booking/<int:pk>/delete", views.BookingDeleteView.as_view(), name="booking_delete"),
    # Booking update
    path("user/booking/<int:pk>/update", views.BookingUpdateView.as_view(), name="booking_update"),
]
