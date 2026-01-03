from django.contrib import admin
from .models import Genre, GameSystem, NPCTable, NPCTableEntry

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(GameSystem)
class GameSystemAdmin(admin.ModelAdmin):
    list_display = ("name", "genre", "is_active", "sort_order", "slug")
    list_filter = ("genre", "is_active")
    list_editable = ("is_active", "sort_order")
    prepopulated_fields = {"slug": ("name",)}

class NPCTableEntryInline(admin.TabularInline):
    model = NPCTableEntry
    extra = 10

@admin.register(NPCTable)
class NPCTableAdmin(admin.ModelAdmin):
    list_display = ("label", "key", "game")
    list_filter = ("game",)
    inlines = [NPCTableEntryInline]