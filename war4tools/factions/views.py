from django.shortcuts import render, get_object_or_404
from .models import Faction

# Create your views here.
def faction_list(request):
    factions = Faction.objects.filter(is_active=True).order_by("name")
    return render(request, "factions/faction_list.html", {"factions": factions})

def faction_detail(request, slug):
    faction = get_object_or_404(Faction, slug=slug, is_active=True)
    return render(request, "factions/faction_detail.html", {"faction": faction})