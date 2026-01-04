from django.urls import path
from . import views

app_name = "factions"

urlpatterns = [
    path("", views.faction_list, name="list"),
    path("<slug:slug>/", views.faction_detail, name="detail"),
]