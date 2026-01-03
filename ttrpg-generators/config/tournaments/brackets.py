import math
from django.db import transaction
from .models import Match
from .services import report_winner  # for auto-advance
from .seeding import apply_random_seeding


def next_power_of_two(n: int) -> int:
    return 1 if n <= 1 else 2 ** math.ceil(math.log2(n))


def losers_match_count_power_of_two(size: int, losers_round: int) -> int:
    """
    Losers bracket rounds = 2*log2(size) - 1
    Match count pattern (size power-of-two):
      8:  [2,2,1,1,1]
      16: [4,4,2,2,1,1,1]
      32: [8,8,4,4,2,2,1,1,1]
    Generic formula produces that pattern.
    """
    if size < 4 or (size & (size - 1)) != 0:
        raise ValueError("size must be a power of two >= 4")

    pair_index = (losers_round + 1) // 2  # 1,1,2,2,3,3...
    count = size // (2 ** (pair_index + 1))
    return max(1, count)


def auto_advance_byes(tournament):
    for match in tournament.matches.filter(is_complete=False):
        if match.a and not match.b:
            report_winner(match, match.a)
        elif match.b and not match.a:
            report_winner(match, match.b)


@transaction.atomic
def create_double_elim_bracket(tournament, entries):
    if tournament.is_locked:
        raise ValueError("Tournament already seeded / locked")
    """
    Creates a full double-elimination bracket for sizes up to 32 (power-of-two padding).
    """
    entries = apply_random_seeding(entries)

    n = len(entries)
    size = next_power_of_two(n)
    if size not in (4, 8, 16, 32):
        raise ValueError("Supported bracket sizes: 4, 8, 16, 32")

    padded = entries[:] + [None] * (size - n)

    winners_rounds = int(math.log2(size))
    losers_rounds = 2 * winners_rounds - 1

    winners = {}  # (round, match) -> Match
    losers = {}   # (round, match) -> Match

    # -------------------------
    # Create Winners matches
    # -------------------------
    for r in range(1, winners_rounds + 1):
        match_count = size // (2 ** r)
        for m in range(1, match_count + 1):
            winners[(r, m)] = Match.objects.create(
                tournament=tournament,
                bracket="W",
                round_number=r,
                match_number=m,
            )

    # Fill Winners Round 1
    for m in range(1, (size // 2) + 1):
        match = winners[(1, m)]
        match.a = padded[(m - 1) * 2]
        match.b = padded[(m - 1) * 2 + 1]
        match.save()

    # Wire Winners next_winner
    for r in range(1, winners_rounds):
        match_count = size // (2 ** r)
        for m in range(1, match_count + 1):
            cur = winners[(r, m)]
            nxt = winners[(r + 1, (m + 1) // 2)]
            cur.next_winner = nxt
            cur.next_winner_slot = "A" if (m % 2 == 1) else "B"
            cur.save()

    # -------------------------
    # Create Losers matches
    # -------------------------
    for r in range(1, losers_rounds + 1):
        match_count = losers_match_count_power_of_two(size, r)
        for m in range(1, match_count + 1):
            losers[(r, m)] = Match.objects.create(
                tournament=tournament,
                bracket="L",
                round_number=r,
                match_number=m,
            )

    # -------------------------
    # Wire Losers progression (within losers bracket)
    # -------------------------
    # odd r: pair winners into next round (A/B)
    # even r: advance 1:1 into next round slot A (slot B reserved for WB drops)
    for r in range(1, losers_rounds):
        cur_count = losers_match_count_power_of_two(size, r)

        if r % 2 == 1:
            for m in range(1, cur_count + 1):
                cur = losers[(r, m)]
                nxt = losers[(r + 1, (m + 1) // 2)]
                cur.next_winner = nxt
                cur.next_winner_slot = "A" if (m % 2 == 1) else "B"
                cur.save()
        else:
            for m in range(1, cur_count + 1):
                cur = losers[(r, m)]
                nxt = losers.get((r + 1, m))
                cur.next_winner = nxt
                cur.next_winner_slot = "A"
                cur.save()

    # -------------------------
    # Wire Winners losers dropping into Losers bracket
    # -------------------------
    # WB R1 losers -> LB R1 slot A
    wb_r1_count = size // 2
    lb_r1_count = losers_match_count_power_of_two(size, 1)
    for m in range(1, min(wb_r1_count, lb_r1_count) + 1):
        w = winners[(1, m)]
        l = losers[(1, m)]
        w.next_loser = l
        w.next_loser_slot = "A"
        w.save()

    # WB R2+ losers -> LB even rounds (2r-2) slot B
    for r in range(2, winners_rounds + 1):
        wb_count = size // (2 ** r)
        lb_round = 2 * r - 2  # even round
        if lb_round > losers_rounds:
            continue

        lb_count = losers_match_count_power_of_two(size, lb_round)
        for m in range(1, min(wb_count, lb_count) + 1):
            w = winners[(r, m)]
            l = losers[(lb_round, m)]
            w.next_loser = l
            w.next_loser_slot = "B"
            w.save()

    # -------------------------
    # Grand Final
    # -------------------------
    grand_final = Match.objects.create(
        tournament=tournament,
        bracket="G",
        round_number=1,
        match_number=1,
    )

    winners_final = winners[(winners_rounds, 1)]
    losers_final = losers[(losers_rounds, 1)]

    winners_final.next_winner = grand_final
    winners_final.next_winner_slot = "A"
    winners_final.save()

    losers_final.next_winner = grand_final
    losers_final.next_winner_slot = "B"
    losers_final.save()

    # -------------------------
    # Auto-advance byes
    # -------------------------
    auto_advance_byes(tournament)

    tournament.is_locked = True
    tournament.save(update_fields=["is_locked"])