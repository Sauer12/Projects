from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Reservation

@login_required
def my_reservations(request):
    qs = (
        Reservation.objects
        .filter(user=request.user)
        .select_related("showtime__movie", "showtime__hall")
        .order_by("-created_at")
    )
    return render(request, "cinema/my_reservations.html", {"reservations": qs})

@login_required
def cancel_reservation(request, pk: int):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    # zrušíme celú rezerváciu (vymaže aj ReservationSeat cez CASCADE => sedadlá sa uvoľnia)
    reservation.delete()
    messages.success(request, "Rezervácia bola zrušená.")
    return redirect("cinema:my_reservations")
