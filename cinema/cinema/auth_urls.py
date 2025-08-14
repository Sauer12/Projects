from django.urls import path
from .views_auth import SignUpView

app_name = "auth_custom"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]