from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from .forms import SignUpForm

User = get_user_model()

class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")  # po registrácii presmerujeme na homepage

    def form_valid(self, form):
        response = super().form_valid(form)
        # automaticky prihlásime nového používateľa po registrácii
        login(self.request, self.object)
        return response