from django.contrib import admin
from .models import Movie, Hall, Seat, Showtime, Reservation, ReservationSeat

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "director", "year")
    search_fields = ("title", "director")

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    readonly_fields = ("row_label", "seat_number")
    can_delete = False

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("name", "rows", "cols", "seats_count")
    inlines = [SeatInline]

    def seats_count(self, obj):
        return obj.seats.count()

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ("movie", "hall", "start_at")
    list_filter = ("hall", "movie", "start_at")

class ReservationSeatInline(admin.TabularInline):
    model = ReservationSeat
    extra = 0

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "showtime", "status", "created_at", "seats_list")
    list_filter = ("status", "showtime__hall", "showtime__movie")
    inlines = [ReservationSeatInline]

    def seats_list(self, obj: Reservation):
        return obj.seats_labels

@admin.register(ReservationSeat)
class ReservationSeatAdmin(admin.ModelAdmin):
    list_display = ("reservation", "showtime", "seat")
    list_filter = ("showtime", "seat__hall")