from django.db import models
from django.utils import timezone

FACTIONS_IN_40K = [
    ("space_marines", "Space Marines"),
    ("black_templar", "Black Templar"),
    ("blood_angels", "Blood Angels"),
    ("dark_angels", "Dark Angels"),
    ("deathwatch", "Deathwatch"),
    ("grey_knights", "Grey Knights"),
    ("space_wolves", "Space Wolves"),
    ("adepta_sororitas", "Adepta Sororitas"),
    ("adeptus_custodes", "Adeptus Custodes"),
    ("adeptus_mechanicus", "Adeptus Mechanicus"),
    ("astra_militarum", "Astra Militarum"),
    ("chaos_space_marines", "Chaos Space Marines"),
    ("death_guard", "Death Guard"),
    ("thousand_sons", "Thousand Sons"),
    ("world_eaters", "World Eaters"),
    ("emperors_children", "Emperor's Children"),
    ("chaos_daemons", "Chaos Daemons"),
    ("aeldari", "Aeldari"),
    ("drukhari", "Drukhari"),
    ("tyranids", "Tyranids"),
    ("genestealer_cults", "Genestealer Cults"),
    ("leagues_of_votann", "Leagues of Votann"),
    ("necrons", "Necrons"),
    ("orks", "Orks"),
    ("tau_empire", "T'au Empire"),
]

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Player(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Entry(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="entries")
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    faction = models.CharField(max_length=100, choices=FACTIONS_IN_40K, default="space_marines")
    detachment = models.CharField(max_length=100)
    seed = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("tournament", "player")

    def __str__(self):
        return f"{self.player} ({self.faction} - {self.detachment})"
    
class Match(models.Model):
    BRACKET_CHOICES = [
        ("W", "Winners"),
        ("L", "Losers"),
        ("G", "Grand Final"),
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="matches")
    bracket = models.CharField(max_length=1, choices=BRACKET_CHOICES)

    round_number = models.PositiveIntegerField()
    match_number = models.PositiveIntegerField()

    a = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True, blank=True, related_name="match_a_set")
    b = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True, blank=True, related_name="match_b_set")

    winner = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True, blank=True, related_name="match_wins")
    is_complete = models.BooleanField(default=False)

    next_winner = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="feeds_wins")
    next_winner_slot = models.CharField(max_length=1, choices=[("A","A"), ("B", "B")], null=True, blank=True)

    next_loser = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="feeds_loses")
    next_loser_slot = models.CharField(max_length=1, choices=[("A","A"), ("B", "B")], null=True, blank=True)

    scheduled_for = models.DateTimeField(null=True, blank=True)

    seed = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("tournament", "bracket", "round_number", "match_number")
        ordering = ["tournament_id", "bracket", "round_number", "match_number"]

    def __str__(self):
        return f"{self.tournament} {self.bracket}{self.round_number}-{self.match_number}"