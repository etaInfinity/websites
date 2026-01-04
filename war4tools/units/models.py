from django.db import models
from factions.models import Faction


class UnitType(models.TextChoices):
    CHARACTERS = "CHARACTERS", "Characters"
    BATTLELINE = "BATTLELINE", "Battleline"
    DEDICATED_TRANSPORT = "DEDICATED_TRANSPORT", "Dedicated Transport"
    OTHER = "OTHER", "Other"


class Unit(models.Model):
    faction = models.ForeignKey(
        Faction,
        on_delete=models.CASCADE,
        related_name="units",
    )

    name = models.CharField(max_length=160)

    unit_type = models.CharField(
        max_length=32,
        choices=UnitType.choices,
        default=UnitType.OTHER,
    )

    # Core stats (10th style)
    movement = models.PositiveIntegerField(help_text="Inches (e.g. 6.0)")
    toughness = models.PositiveSmallIntegerField()
    armour_save = models.PositiveSmallIntegerField(help_text="Armour save as a number (e.g. 3 for 3+)")
    wounds = models.PositiveSmallIntegerField()
    leadership = models.PositiveSmallIntegerField(help_text="Leadership as a number (e.g. 6 for 6+)")
    objective_control = models.PositiveSmallIntegerField()

    points_cost = models.PositiveIntegerField(help_text="Points per unit (or per model if you prefer—just be consistent).")

    invulnerable_save = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Invuln save as a number (e.g. 4 for 4+). Leave blank if none.",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["faction__name", "unit_type", "name"]
        constraints = [
            models.UniqueConstraint(fields=["faction", "name"], name="uniq_unit_per_faction_name")
        ]

    def __str__(self):
        return f"{self.name} ({self.faction.name})"