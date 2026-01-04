from django.contrib import admin
from .models import Faction
from units.models import Unit


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0
    fields = (
        "name", "unit_type", "points_cost",
        "movement", "toughness", "armour_save", "wounds", "leadership", "objective_control",
        "invulnerable_save", "is_active",
    )
    show_change_link = True


@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [UnitInline]