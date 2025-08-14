# cinema/views_seating.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction, IntegrityError

from .models import Showtime, Reservation, ReservationSeat, Seat


@require_http_methods(["GET"])
def showtime_seats(request, showtime_id: int):
    """
    GET: Zobrazí mapu sedadiel pre daný showtime.
    BOOKED sedadlá sú odvodené z ReservationSeat (showtime, seat).
    """
    st = get_object_or_404(
        Showtime.objects.select_related("movie", "hall"),
        pk=showtime_id
    )
    hall = st.hall

    # všetky obsadené (booked) sedadlá pre tento showtime
    booked_pairs = set(
        ReservationSeat.objects.filter(showtime=st)
        .values_list("seat__row_label", "seat__seat_number")
    )

    # priprav 2D grid
    grid = []
    for r in range(hall.rows):
        row_label = chr(ord("A") + r)
        row_cells = []
        for c in range(1, hall.cols + 1):
            is_booked = (row_label, c) in booked_pairs
            row_cells.append({
                "label": f"{row_label}{c}",
                "row": row_label,
                "num": c,
                "booked": is_booked,
            })
        grid.append({"row_label": row_label, "cells": row_cells})

    ctx = {
        "showtime": st,
        "movie": st.movie,
        "hall": hall,
        "grid": grid,
    }
    return render(request, "cinema/showtime_seats.html", ctx)


@login_required
@require_http_methods(["POST"])
def reserve_seats(request, showtime_id: int):
    """
    POST: Uloží rezerváciu pre prihláseného používateľa.
    Očakáva parametre: seats=A1&seats=A2&...
    Uloženie prebieha v transakcii, chytáme IntegrityError (duplicitné sedadlá).
    """
    st = get_object_or_404(
        Showtime.objects.select_related("hall", "movie"),
        pk=showtime_id
    )
    hall = st.hall

    labels = request.POST.getlist("seats")  # napr. ["A1","B5","C10"]
    if not labels:
        messages.error(request, "Nevybral si žiadne sedadlá.")
        return redirect("seating:showtime_seats", showtime_id=showtime_id)

    # Parse "A10" -> ("A", 10) ; zvládne aj "AA10"
    parsed = []
    for lab in labels:
        i = 0
        while i < len(lab) and lab[i].isalpha():
            i += 1
        row = lab[:i].upper()
        num_str = lab[i:]
        if not row or not num_str.isdigit():
            messages.error(request, f"Neplatný formát sedadla: {lab}")
            return redirect("seating:showtime_seats", showtime_id=showtime_id)
        parsed.append((row, int(num_str)))

    # Over, že sedadlá existujú v tejto sále
    seats = list(Seat.objects.filter(hall=hall))
    seat_map = {(s.row_label, s.seat_number): s for s in seats}
    try:
        seat_objs = [seat_map[(r, n)] for (r, n) in parsed]
    except KeyError:
        messages.error(request, "Vybral si sedadlo, ktoré v tejto sále neexistuje.")
        return redirect("seating:showtime_seats", showtime_id=showtime_id)

    # Ulož v transakcii (ochrana pred závodom)
    try:
        with transaction.atomic():
            reservation = Reservation.objects.create(
                user=request.user,
                showtime=st,
                status="CONFIRMED",
            )
            # Skús rýchly bulk insert
            rows = [
                ReservationSeat(reservation=reservation, showtime=st, seat=s)
                for s in seat_objs
            ]
            ReservationSeat.objects.bulk_create(rows)
    except IntegrityError:
        # Niekto medzitým zobral niektoré z tých sedadiel
        messages.error(
            request,
            "Niektoré z vybraných sedadiel už boli práve rezervované iným používateľom. "
            "Vyber prosím iné sedadlá."
        )
        return redirect("seating:showtime_seats", showtime_id=showtime_id)

    messages.success(request, f"Rezervácia vytvorená: {', '.join(labels)}")
    return redirect("cinema:my_reservations")
