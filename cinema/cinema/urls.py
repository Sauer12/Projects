from django.urls import path
from . import views_movies, views_profile

app_name = "cinema"

urlpatterns = [
    path("movies/", views_movies.MovieListView.as_view(), name="movie_list"),
    path("movies/<int:pk>/", views_movies.MovieDetailView.as_view(), name="movie_detail"),
    path("me/reservations/", views_profile.my_reservations, name="my_reservations"),
    path("me/reservations/<int:pk>/cancel/", views_profile.cancel_reservation, name="cancel_reservation"),
]


