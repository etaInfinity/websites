from django.urls import path
from . import views

urlpatterns = [
    path("", views.tournament_index, name="tournament_index"),
    path("t/<int:tournament_id>/", views.tournament_bracket, name="tournament_bracket"),
    path("t/<int:tournament_id>/players/", views.manage_entries, name="manage_entries"),
    path("t/<int:tournament_id>/generate/", views.generate_bracket, name="generate_bracket"),
    path("match/<int:match_id>/winner/", views.set_match_winner, name="set_match_winner"),
]