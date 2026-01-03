import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from .models import Genre, GameSystem
from .services.registry import get_generator
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
@ensure_csrf_cookie
def npc_generator_page(request):
    genres = Genre.objects.all().order_by("name")
    return render(request, "npcgen/npc_generator.html", {"genres": genres})

@require_GET
def api_games_for_genre(request):
    genre_slug = request.GET.get("genre")
    if not genre_slug:
        return HttpResponseBadRequest("Missing Genre")
    genre = get_object_or_404(Genre, slug=genre_slug)
    games = genre.games.filter(is_active=True).order_by("sort_order", "name")
    return JsonResponse({
        "genre": {"name": genre.name, "slug": genre.slug},
        "games": [{"name": g.name, "slug": g.slug} for g in games]
    })

@require_POST
def api_generate_npc(request):
    print("RAW BODY:", request.body)
    print("CONTENT TYPE:", request.content_type)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception as e:
        print("JSON DECODE ERROR:", e)
        return HttpResponseBadRequest("Invalid JSON")

    print("PARSED PAYLOAD:", payload, type(payload))

    game_slug = (payload.get("game") or "").strip()
    print("GAME SLUG:", repr(game_slug))

    if not game_slug:
        return HttpResponseBadRequest("Missing game")

    game = get_object_or_404(GameSystem, slug=game_slug, is_active=True)

    try:
        generator = get_generator(game.slug)
    except KeyError as e:
        return HttpResponseBadRequest(str(e))

    npc = generator.generate()
    return JsonResponse({"game": {"name": game.name, "slug": game.slug}, "npc": npc.to_dict()})