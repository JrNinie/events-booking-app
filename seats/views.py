# coding: utf-8

"""
Views Module
"""

# Django imports
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView

# Model imports
from .models import Room, Seat, Event, Seatbooking

# Form imports
from .forms import RoomSelectionForm, EventSelectionForm


@login_required
def index(request):
    """
    Events view
    """
    # On room selection
    if request.method == "POST":

        event_id = request.POST.get("event")
        room_id = Event.objects.get(id=event_id).room.id
        response = redirect(f"event/{event_id}/room/{room_id}/")
        return response
    else:

        # Load template
        template = loader.get_template("seats/index.html")

        # Create form
        event_selection_form = EventSelectionForm()

        # Fill context
        context = {
            "event_selection_form": event_selection_form,
        }

        # Serve HTTP response
        return HttpResponse(template.render(context, request))


@login_required
def room(request, room_id, event_id):
    """
    Seats view
    """
    # Load template
    template = loader.get_template("seats/room.html")

    # Get current room object
    room = Room.objects.get(pk = room_id)

    # Get seats for this room
    seat_objects = room.seats.all()

    # Get availability status of each seat for this event
    available = [seat.is_available(event_id) for seat in seat_objects]

    # Zip the two lists
    seats = zip(seat_objects, available)

    # Fill context
    context = {
        "room": room,
        "seats": seats,
        "event": Event.objects.get(pk=event_id)
    }

    # Serve HTTP response
    return HttpResponse(template.render(context, request))


@login_required
def seat_selection(request, room_id, seat_ids, event_id):
    """
    Seat selection view
    """
    # Load template
    template = loader.get_template("seats/seat_selection.html")

    seat_id_list = seat_ids.split("_") # attention: seat_id is Seat.identifier

    # Record booking info (in model Seatbooking)
    event = Event.objects.get(pk=event_id)
    for seat_id in seat_id_list:
        seat = Seat.objects.get(identifier=seat_id)
        seatbooking = Seatbooking(event=event, seat=seat, user=request.user)
        seatbooking.save()

    # Fill context
    context = {
        "seat_id_list": seat_id_list,
    }

    # Serve HTTP response
    return HttpResponse(template.render(context, request))


@method_decorator(login_required, name="dispatch") # can not use @login_required it's class not def
class BookingView(generic.ListView):
    template_name = "seats/booking.html"
    context_object_name = "user_seatbooking_list"

    def get_queryset(self):
        """Get current users seat booking

        Returns:
            queryset: current users seat booking info
        """
        return Seatbooking.objects.filter(user=self.request.user.id)


@method_decorator(login_required, name="dispatch")
class BookingDeleteView(DeleteView):
    # Defautl template name is "seatbooking_confirm_delete.html"
    model = Seatbooking
    # If delete ok, go to booking management page
    success_url = reverse_lazy("seats:booking") # must give a view func or url pattern

    # Custom POST in order to add cancel buttom
    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.success_url
            return redirect(url)
        else: # Confirm cancel
            return super(BookingDeleteView, self).post(request, *args, **kwargs)


class BookingUpdateView(UpdateView):
    model = Seatbooking
    fields = ["event", "seat"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("seats:booking")