# coding: utf-8

"""
# Models module

Define models that will be stored in the database


# Get Django user class
>>> user_type = settings.AUTH_USER_MODEL
"""

# MongoDB connector for django
from djongo import models

# Get django user model
from django.conf import settings

from django.utils import timezone

class Room(models.Model):
    """
    Room class

    Define a room with seats.
    """
    name = models.CharField(max_length=255, unique=True)

    # When displaying class object as a string,
    # display a custom string for readibility
    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Event class

    Define an event with name, date and description
    """
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField(null=True)

    class Meta:
        unique_together = ('room', 'date')

    # When displaying class object as a string,
    # display a custom string for readibility
    def __str__(self):
        return f"{self.name} : {self.date}"


class Seat(models.Model):
    """
    Seat class

    Define a seat with an ID and a x and y position.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name = "seats", default = None)
    events = models.ManyToManyField(Event, through="Seatbooking")

    # Seat fields
    identifier = models.CharField(max_length=255)

    # Seat position
    x = models.FloatField()
    y = models.FloatField()

    # When displaying class object as a string,
    # display a custom string for readibility
    def __str__(self):
        return f"{self.identifier} @ x = {self.x} & y = {self.y}"

    def is_available(self, event_id):
        """If this seat for a certain event is available

        Returns:
            boolean: True(available) or False(not available)
        """
        return False if Seatbooking.objects.filter(seat=self.id, event=event_id) else True 


class Seatbooking(models.Model):
    """
    Seatbooking class

    Define the seat booking for an event by an user
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        # Ensure a seat for a certain event can only be booked once
        unique_together = ('event', 'seat')

    def __str__(self):
        return f"user{self.user} booked seat{self.seat} for event{self.event} "

