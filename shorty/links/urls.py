from django.urls import path
from .views import create_link, follow, list_links

urlpatterns = [
    path("", create_link, name="create_link"),
    path("links/", list_links, name="list_links"),
    path("<slug:slug>/", follow, name="follow"),  # musí byť až za "" routou
]

