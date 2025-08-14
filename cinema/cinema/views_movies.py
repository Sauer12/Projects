from django.views.generic import ListView, DetailView
from .models import Movie

class MovieListView(ListView):
    model = Movie
    template_name = "cinema/movie_list.html"
    context_object_name = "movies"

class MovieDetailView(DetailView):
    model = Movie
    template_name = "cinema/movie_detail.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # zoradíme predstavenia podľa času
        ctx["showtimes"] = self.object.showtimes.select_related("hall").order_by("start_at")
        return ctx
