from django.urls import path
from .views_seating import showtime_seats, reserve_seats


app_name = "seating"

urlpatterns = [
    path("showtimes/<int:showtime_id>/seats/", showtime_seats, name="showtime_seats"),
    path("showtimes/<int:showtime_id>/reserve/", reserve_seats, name="reserve_seats"),
]

