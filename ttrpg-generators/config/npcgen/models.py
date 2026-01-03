from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    def __str__(self):
        return self.name
    
class GameSystem(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="games")
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["genre__name", "sort_order", "name"]
        unique_together = [("genre", "name")]

    def __str__(self):
        return f"{self.genre.name} - {self.name}"
    
class NPCTable(models.Model):
    """
    A named table for a specific game: roles, quirks, goals, factions, etc.
    """
    game = models.ForeignKey(GameSystem, on_delete=models.CASCADE, related_name="tables")
    key = models.SlugField(max_length=80)
    label = models.CharField(max_length=120)

    class Meta:
        unique_together = [("game", "key")]

    def __str__(self):
        return f"{self.game.slug}:{self.key}"
    
class NPCTableEntry(models.Model):
    table = models.ForeignKey(NPCTable, on_delete=models.CASCADE, related_name="entries")
    text = models.CharField(max_length=240)
    weight = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.table} - {self.text}"