from django.contrib import admin
from .models import Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "faction",
        "unit_type",
        "points_cost",
        "movement",
        "toughness",
        "armour_save",
        "wounds",
        "leadership",
        "objective_control",
        "invulnerable_save",
        "is_active",
    )
    list_filter = ("faction", "unit_type", "is_active")
    search_fields = ("name", "faction__name")
    ordering = ("faction__name", "unit_type", "name")

    fieldsets = (
        ("Identity", {"fields": ("faction", "name", "unit_type", "is_active")}),
        ("Stats", {"fields": (
            "movement",
            "toughness",
            "armour_save",
            "wounds",
            "leadership",
            "objective_control",
            "invulnerable_save",
        )}),
        ("Points", {"fields": ("points_cost",)}),
    )