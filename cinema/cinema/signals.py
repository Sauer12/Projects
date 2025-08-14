from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Hall, Seat

@receiver(post_save, sender=Hall)
def generate_seats_on_hall_create(sender, instance: Hall, created, **kwargs):
    if not created:
        return
    seats = []
    for r in range(instance.rows):
        row_label = chr(ord('A') + r)
        for c in range(instance.cols):
            seats.append(Seat(hall=instance, row_label=row_label, seat_number=c + 1))
    Seat.objects.bulk_create(seats)