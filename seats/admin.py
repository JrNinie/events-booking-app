# coding: utf-8

"""
Admin module
"""

from django.contrib import admin
from .models import Room, Seat, Event, Seatbooking


class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "name", "description", "date")
    ordering = ("-date",)


class SeatAdmin(admin.ModelAdmin):
    list_display = ("id","identifier", "x", "y")


class SeatbookingAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "seat", "user")

admin.site.register(Seat, SeatAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Seatbooking, SeatbookingAdmin)
admin.site.register(Room, RoomAdmin)
