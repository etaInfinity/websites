import random
from typing import Dict, Type, Optional
from django.db.models import Sum
from npcgen.models import GameSystem, NPCTable
from .base import BaseNPCGenerator

GENERATOR_REGISTRY: Dict[str, Type[BaseNPCGenerator]] = {}

def register(generator_cls: Type[BaseNPCGenerator]):
    GENERATOR_REGISTRY[generator_cls.game_slug] = generator_cls
    return generator_cls

def get_generator(game_slug: str) -> BaseNPCGenerator:
    cls = GENERATOR_REGISTRY.get(game_slug)
    if not cls:
        raise KeyError(f"No Generator registered for game: '{game_slug}'.")
    return cls()

def pick_weighted(rng: random.Random, table: NPCTable) -> str:
    entries = list(table.entries.all())
    if not entries:
        return "-"
    total = sum(e.weight for e in entries)
    roll = rng.randint(1, total)
    running = 0
    for e in entries:
        running += e.weight
        if roll <= running:
            return e.text
    return entries[-1].text

def get_table(game: GameSystem, key: str) -> NPCTable:
    return NPCTable.objects.get(game=game, key=key)