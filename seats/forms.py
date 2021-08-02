# coding: utf-8

"""
# Forms module

Define custom forms used in the apps
"""

# Django imports
from django import forms

# Map models imports
from .models import Room, Seat, Event


class SeatForm(forms.ModelForm):
    """
    Model form linked to Seat model
    """
    class Meta:
        model = Seat
        fields = ["identifier", "x", "y"]


class RoomSelectionForm(forms.Form):
    """
    Classic form linked to rooms
    """
    room = forms.ModelChoiceField(queryset=Room.objects.all().order_by('name'))


class EventSelectionForm(forms.Form):
    """
    Classic form linked to events
    """
    event = forms.ModelChoiceField(queryset=Event.objects.all().order_by("date"), empty_label="Please choose an event")