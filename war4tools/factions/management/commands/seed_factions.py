from django.core.management.base import BaseCommand
from factions.models import Faction

DEFAULT_FACTIONS = [
    ("Adeptus Astartes", "The Emperor's finest super-human warriors"),
    ("Astra Militarum", "The armies of mankind: tanks, artillery, and endless troops."),
    ("Adepta Sororitas", "Zealous warrior-nuns with holy fire and power armour."),
    ("Adeptus Mechanicus", "Tech-priests and cyborg legions of Mars."),
    ("Chaos Space Marines", "Traitor Astartes devoted to the Dark Gods."),
    ("Death Guard", "Nurgle’s plague-marines: resilient and rotten."),
    ("Thousand Sons", "Sorcerers, rubricae, and warp-fueled schemes."),
    ("World Eaters", "Khorne’s berserkers: melee brutality."),
    ("Aeldari", "Fast, elite, and lethal ancient space elves."),
    ("Drukhari", "Raiders and sadists from Commorragh."),
    ("Orks", "Green tide mayhem: loud, brutal, and unstoppable."),
    ("T’au Empire", "Advanced tech and combined-arms firepower."),
    ("Necrons", "Ancient immortal machines awakening to reclaim the galaxy."),
    ("Tyranids", "The all-consuming hive fleets."),
    ("Genestealer Cults", "Insurrectionists and alien cult uprisings."),
    ("Leagues of Votann", "Hardy kin with ruthless pragmatism and advanced gear."),
]

class Command(BaseCommand):
    help = "Seed the database with starter Warhammer 40K factions."

    def handle(self, *args, **options):
        created = 0
        for name, desc in DEFAULT_FACTIONS:
            obj, was_created = Faction.objects.get_or_create(
                name=name,
                defaults={"description": desc, "is_active": True},
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Created {created} faction(s)."))