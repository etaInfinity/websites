from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
from .models import Tournament, Match, Entry
from .services import report_winner
from .brackets import create_double_elim_bracket
from .forms import EntryForm

@require_http_methods(["GET", "POST"])
def manage_entries(request, tournament_id):
    t = get_object_or_404(Tournament, id=tournament_id)

    if t.is_locked:
        messages.error(request, "Tournament is locked. You can't add players.")
        return redirect("tournament_bracket", tournament_id=t.id)

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.tournament = t
            entry.save()
            return redirect("manage_entries", tournament_id=t.id)
    else:
        form = EntryForm()

    entries = t.entries.select_related("player").order_by("seed", "player__name")
    return render(request, "tournaments/manage_entries.html", {
        "tournament": t,
        "form": form,
        "entries": entries,
    })

# Create your views here.
def tournament_bracket(request, tournament_id):
    t = get_object_or_404(Tournament, id=tournament_id)

    matches = t.matches.select_related("a__player", "b__player", "winner__player").all()

    return render(request, "tournaments/bracket.html", {
        "tournament": t,
        "matches": matches,
    })

def tournament_index(request):
    tournaments = Tournament.objects.order_by("-created_at")
    return render(request, "tournaments/index.html", {"tournaments": tournaments})

@require_POST
@transaction.atomic
def set_match_winner(request, match_id):
    try:
        match = get_object_or_404(Match, id=match_id)

        winner_entry_id = request.POST.get("winner_entry_id")
        if not winner_entry_id:
            return JsonResponse({"error": "winner_entry_id required"}, status=400)

        winner = get_object_or_404(Entry, id=winner_entry_id, tournament=match.tournament)

        # This should do all DB writes (and will rollback if we error later)
        report_winner(match, winner)

        updated = match.tournament.matches.select_related(
            "a__player", "b__player", "winner__player"
        ).all()

        payload = [{
            "id": m.id,
            "bracket": m.bracket,
            "round": m.round_number,
            "match": m.match_number,
            "a": entry_payload(m.a),
            "b": entry_payload(m.b),
            "winner_id": m.winner_id,
            "is_complete": m.is_complete,
        } for m in updated]

        return JsonResponse({"matches": payload}, status=200)

    except Exception as e:
        # IMPORTANT: because of @transaction.atomic, DB changes rollback on exception
        return JsonResponse({"error": str(e)}, status=500)

def entry_payload(e):
    if not e:
        return None
    return {
        "id": e.id,
        "player": e.player.name,
        "faction": e.faction,
        "detachment": e.detachment,
    }

@require_POST
def generate_bracket(request, tournament_id):
    t = get_object_or_404(Tournament, id=tournament_id)

    if t.is_locked:
        return HttpResponseBadRequest("Tournament already locked / seeded")

    entries = list(t.entries.select_related("player").all())  # uses related_name="entries"
    if len(entries) < 2:
        return HttpResponseBadRequest("Need at least 2 entries to generate a bracket")

    create_double_elim_bracket(t, entries)
    return redirect("tournament_bracket", tournament_id=t.id)