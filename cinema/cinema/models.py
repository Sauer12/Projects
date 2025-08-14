from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
User = get_user_model()

class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=200, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year})" if self.year else self.title

class Hall(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rows = models.PositiveIntegerField(help_text="Number of seat rows (e.g. 8)")
    cols = models.PositiveIntegerField(help_text="Seats per row (e.g. 12)")

    def __str__(self):
        return f"Hall {self.name} ({self.rows}x{self.cols})"

    def seat_label(self, row_index: int, col_index: int) -> str:
        """
        row_index: 0-based -> 'A', 'B', ...
        col_index: 0-based -> 1..N
        """
        row_label = chr(ord('A') + row_index)
        return f"{row_label}{col_index + 1}"

class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="seats")
    row_label = models.CharField(max_length=2)  # 'A', 'B', ...
    seat_number = models.PositiveIntegerField()  # 1..N

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hall", "row_label", "seat_number"],
                name="uniq_seat_per_hall"
            )
        ]

    def __str__(self):
        return f"{self.hall.name}:{self.row_label}{self.seat_number}"

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT, related_name="showtimes")
    start_at = models.DateTimeField()

    class Meta:
        ordering = ["start_at"]

    def __str__(self):
        return f"{self.movie} @ {self.hall.name} — {self.start_at:%Y-%m-%d %H:%M}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name="reservations")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="CONFIRMED")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reservation #{self.id} by {self.user} for {self.showtime}"

    @property
    def seats_labels(self):
        return ", ".join(rs.seat_label for rs in self.reservation_seats.all())

class ReservationSeat(models.Model):
    """
    Through tabuľka: jedna rezervácia môže mať viac sedadiel.
    Kvôli DB-unikátnosti naprieč všetkými rezerváciami v rámci jedného showtime
    držíme aj priamy FK na showtime (denormalizácia pre UNIQUE constraint).
    """
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="reservation_seats")
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name="reservation_seats")
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT, related_name="reservation_seats")

    class Meta:
        constraints = [
            # žiadne duplikáty v rámci tej istej rezervácie
            models.UniqueConstraint(fields=["reservation", "seat"], name="uniq_seat_in_reservation"),
            # žiadna druhá rezervácia na to isté sedadlo pre ten istý showtime
            models.UniqueConstraint(fields=["showtime", "seat"], name="uniq_seat_per_showtime"),
        ]

    def clean(self):
        # bezpečnostná kontrola: sedadlo musí patriť sále z daného showtime
        if self.showtime.hall_id != self.seat.hall_id:
            from django.core.exceptions import ValidationError
            raise ValidationError("Seat does not belong to the hall of this showtime.")

    @property
    def seat_label(self) -> str:
        return f"{self.seat.row_label}{self.seat.seat_number}"

    def __str__(self):
        return f"{self.reservation} -> {self.seat_label}"