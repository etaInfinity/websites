from django.db import transaction

def _place_entry(match, slot, entry):
    """
    Places entry into match slot A or B.
    Will NOT overwrite an occupied slot with a different entry.
    Skips if match/slot/entry is missing.
    """
    if not match or not slot or entry is None:
        return

    if slot == "A":
        if match.a and match.a_id != entry.id:
            raise ValueError(f"Match {match.id} slot A already occupied.")
        match.a = entry
    elif slot == "B":
        if match.b and match.b_id != entry.id:
            raise ValueError(f"Match {match.id} slot B already occupied.")
        match.b = entry
    else:
        raise ValueError("slot must be 'A' or 'B'")

    match.save()


@transaction.atomic
def report_winner(match, winner_entry):
    if match.is_complete:
        return match

    if winner_entry not in (match.a, match.b):
        raise ValueError("Winner must be one of the participants")

    loser_entry = match.b if winner_entry == match.a else match.a

    match.winner = winner_entry
    match.is_complete = True
    match.save()

    # advance winner
    _place_entry(match.next_winner, match.next_winner_slot, winner_entry)

    # advance loser (skip None)
    _place_entry(match.next_loser, match.next_loser_slot, loser_entry)

    return match