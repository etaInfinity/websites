import random
from .base import BaseNPCGenerator, NPCResult
from .registry import register, pick_weighted, get_table
from npcgen.models import GameSystem

@register
class DnD5eNPCGenerator(BaseNPCGenerator):
    game_slug = "dnd-5e"

    def generate(self, *, seed=None, **opts) -> NPCResult:
        rng = random.Random(seed)
        game = GameSystem.objects.get(slug=self.game_slug)

        return NPCResult(
            name=pick_weighted(rng, get_table(game, "names")),
            species=pick_weighted(rng, get_table(game, "species")),
            role=pick_weighted(rng, get_table(game, "roles")),
            personality=pick_weighted(rng, get_table(game, "personalities")),
            goal=pick_weighted(rng, get_table(game, "goals")),
            quirk=pick_weighted(rng, get_table(game, "quirks")),
            hook=pick_weighted(rng, get_table(game, "hooks")),
            extras={}
        )
    
"""
FOR OTHER GAME SYSTEMS, YOU'D REGISTER OTHER GENERATORS WITH DIFFERENT
TABLE KEYS AND DIFFERENT "EXTRAS"
"""