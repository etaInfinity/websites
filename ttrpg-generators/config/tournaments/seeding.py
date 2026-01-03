# tournaments/seeding.py
import random

def apply_random_seeding(entries):
    """
    Shuffles entries randomly and assigns seed numbers starting at 1.
    """
    entries = list(entries)  # queryset → list
    random.shuffle(entries)

    for i, entry in enumerate(entries, start=1):
        entry.seed = i
        entry.save(update_fields=["seed"])

    return entries