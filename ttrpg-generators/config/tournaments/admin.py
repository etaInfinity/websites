from django.contrib import admin
from .models import Tournament, Player, Entry, Match

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("name", "is_locked", "created_at")
    search_fields = ("name",)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("tournament", "player", "faction", "detachment", "seed")
    list_filter = ("tournament", "faction")
    search_fields = ("player__name", "faction", "detachment")

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("tournament", "bracket", "round_number", "match_number", "is_complete")
    list_filter = ("tournament", "bracket", "is_complete")