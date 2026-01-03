from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import GalaxyGeneratorForm
from .services.generate import generate_galaxy
from .services.map_render import render_galaxy_map_png, render_system_orbits_png

import random
def index(request):
    if request.method == "POST":
        form = GalaxyGeneratorForm(request.POST)
        if form.is_valid():
            size_group = form.cleaned_data["size_group"]
            systems_count = form.cleaned_data["systems_count"]
            seed = form.cleaned_data["seed"]
            if seed is None:
                seed = random.randrange(1, 2_000_000_000)
            return redirect(reverse("galaxy:result", kwargs={"seed": seed}) + f"?size_group={size_group}&systems={systems_count}")
    else:
        form = GalaxyGeneratorForm()

    return render(request, "galaxy/index.html", {"form": form})

# def result(request, seed: int):
#     size_group = request.GET.get("size_group", "mw")
#     systems_count = int(request.GET.get("systems", "10"))
#     data = generate_galaxy(size_group=size_group, systems_count=systems_count, seed=seed)
#     return render(request, "galaxy/result.html", {"data": data})

def result(request, seed: int):
    size_group = request.GET.get("size_group", "mw")
    systems_count = int(request.GET.get("systems", "10"))

    data = generate_galaxy(size_group=size_group, systems_count=systems_count, seed=seed)

    # HARD DEBUG
    print("DEBUG size_group:", size_group)
    print("DEBUG systems_count (from query):", systems_count)
    print("DEBUG generated systems:", len(data["systems"]))
    print("DEBUG first system:", data["systems"][0]["name"] if data["systems"] else None)

    return render(request, "galaxy/result.html", {"data": data})

def map_png(request, seed: int):
    size_group = request.GET.get("size_group", "mw")
    systems_count = int(request.GET.get("systems", "10"))
    label_all = request.GET.get("labels", "1") == "1"

    data = generate_galaxy(size_group=size_group, systems_count=systems_count, seed=seed)
    png = render_galaxy_map_png(data, label_all=label_all)
    return HttpResponse(png, content_type="image/png")

def system_map_png(request, seed: int, system_index: int):
    size_group = request.GET.get("size_group", "mw")
    systems_count = int(request.GET.get("systems", "10"))

    data = generate_galaxy(size_group=size_group, systems_count=systems_count, seed=seed)

    # safety clamp
    system_index = max(0, min(system_index, len(data["systems"]) - 1))
    system = data["systems"][system_index]

    png = render_system_orbits_png(system)
    return HttpResponse(png, content_type="image/png")