from django.urls import path
from . import views

app_name = "npcgen"

urlpatterns = [
    path("", views.npc_generator_page, name="page"),
    path("api/games/", views.api_games_for_genre, name="api_games"),
    path("api/generate/", views.api_generate_npc, name="api_generate"),
]