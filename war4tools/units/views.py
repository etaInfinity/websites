from django.shortcuts import render, get_object_or_404
from .models import Faction

def faction_detail(request, slug):
    faction = get_object_or_404(Faction, slug=slug, is_active=True)
    units = faction.units.filter(is_active=True).order_by("unit_type", "name")
    return render(request, "factions/faction_detail.html", {"faction": faction, "units": units})