import re
import string

MYTHIC = [
    "Astraea","Erebus","Nyx","Helios","Selene","Eos","Ares","Hera","Athena","Apollo",
    "Artemis","Hecate","Nemesis","Atlas","Prometheus","Orpheus","Gaia","Hyperion","Iris","Thanatos",
]

LATINISH = ["Nova","Aurum","Ferrum","Ignis","Umbra","Lumen","Arbor","Mare","Vita","Nox","Caelum","Terra"]

PLACE_PREFIX = ["New", "Port", "Fort", "Lake", "Mount", "Saint", "North", "South", "East", "West"]
PLACE_SUFFIX = ["Haven", "Reach", "Crest", "Harbour", "Point", "Vale", "Ridge", "Cross", "Station", "Outpost"]

GREEK = [
    "Alpha","Beta","Gamma","Delta","Epsilon","Zeta","Eta","Theta","Iota","Kappa",
    "Lambda","Mu","Nu","Xi","Omicron","Pi","Rho","Sigma","Tau","Upsilon","Phi","Chi","Psi","Omega"
]

CONSTELLATIONS = [
    "Aquila","Orion","Lyra","Draco","Cygnus","Vela","Carina","Centaurus","Cassiopeia","Andromeda",
    "Perseus","Scorpius","Sagitta","Phoenix","Hydra","Lupus","Crux","Pavo","Ara","Columba"
]

# Simple “human-ish” syllable banks (not real languages, just good mouthfeel)
SYL_START = ["Ael","Ar","Bel","Cal","Cor","Dar","Eir","Fal","Gar","Hel","Ith","Jar","Kel","Lor","Mor","Nar","Or","Per","Quor","Ral","Sar","Tor","Ul","Val","Vor","Wey","Xan","Yor","Zel"]
SYL_MID   = ["a","e","i","o","u","ae","ia","eo","ou","ar","er","ir","or","ur","an","en","in","on","un","ath","eth","ith","oth","uth","mir","nar","thal","dren","vex","zor"]
SYL_END   = ["a","e","i","o","us","um","on","en","is","ar","or","ia","ys","ara","ion","eus","oth","mir","dell","tor","nax","garde","vane","prime"]


def slugify_caps(s: str) -> str:
    # turn "Alpha Aquila" -> "Alpha Aquila" (light cleanup)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def roman(n: int) -> str:
    # 1..20 is enough for most systems
    vals = [
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    out = []
    while n > 0:
        for v, s in vals:
            if n >= v:
                out.append(s)
                n -= v
                break
    return "".join(out)

def letter_suffix(idx: int) -> str:
    # 0->b, 1->c, ...
    letters = string.ascii_lowercase
    return letters[idx + 1]  # skip 'a'

def make_pronounceable(rng) -> str:
    # 2–3 chunk word, with mild variation
    chunks = rng.randint(2, 3)
    w = rng.choice(SYL_START)
    for _ in range(chunks - 1):
        w += rng.choice(SYL_MID)
    w += rng.choice(SYL_END)
    # clean up occasional double vowels
    w = w.replace("aa", "a").replace("ee", "e").replace("ii", "i").replace("oo", "o").replace("uu", "u")
    return w[0].upper() + w[1:]

def system_designation(rng) -> str:
    """
    Mix of real-ish conventions:
    - 'HD 123456'
    - 'HIP 12345'
    - 'Kepler-442'
    - 'TRAPPIST-1' style
    - 'Gamma Aquilae' style
    """
    scheme = rng.choices(
        ["catalog_hd", "catalog_hip", "mission", "greek_constellation", "two_word"],
        weights=[0.30, 0.18, 0.22, 0.18, 0.12],
        k=1
    )[0]

    if scheme == "catalog_hd":
        return f"HD {rng.randint(10000, 999999)}"
    if scheme == "catalog_hip":
        return f"HIP {rng.randint(1000, 99999)}"
    if scheme == "mission":
        mission = rng.choice(["Kepler", "TOI", "K2", "TESS", "Gaia"])
        if mission == "TOI":
            return f"TOI-{rng.randint(100, 9999)}"
        if mission == "TESS":
            return f"TESS-{rng.randint(100, 9999)}"
        if mission == "Gaia":
            return f"Gaia-{rng.randint(1000, 99999)}"
        return f"{mission}-{rng.randint(10, 999)}"
    if scheme == "greek_constellation":
        return f"{rng.choice(GREEK)} {rng.choice(CONSTELLATIONS)}"
    # two_word
    return f"{make_pronounceable(rng)} {make_pronounceable(rng)}"

def planet_name(rng, system_name: str, idx: int, habitable: bool) -> str:
    """
    Always returns a unique proper name (seeded).
    Habitable worlds get slightly nicer names more often.
    """
    # Bias habitable names toward “cleaner” results (less harsh endings)
    tries = 8
    best = None

    for _ in range(tries):
        n = make_pronounceable(rng)

        # light filtering so names don't look like garbage
        bad = any(x in n.lower() for x in ["q", "xanx", "vv", "kkk"])
        if bad:
            continue

        # habitable: prefer names ending with a vowel or soft consonant
        if habitable:
            if n[-1].lower() in ("a", "e", "i", "o", "u", "n", "s", "r", "l"):
                return n

        best = n

    return best or make_pronounceable(rng)


def planet_designation(system_name: str, idx: int) -> str:
    # Standard: system + b/c/d...
    letters = string.ascii_lowercase
    return f"{system_name} {letters[idx + 1]}"

def proper_planet_name(rng, habitable: bool) -> str:
    """
    Generates a 'real-life-ish' proper name:
    - Mythology names
    - Latin-ish compounds (Nova + word)
    - Place-style names (New Haven / Port Helios)
    - Pronounceable synthetic (your existing make_pronounceable)
    """
    scheme = rng.choices(
        ["mythic", "latin", "place", "synthetic"],
        weights=[0.35, 0.20, 0.15, 0.30] if habitable else [0.25, 0.15, 0.10, 0.50],
        k=1
    )[0]

    if scheme == "mythic":
        return rng.choice(MYTHIC)

    if scheme == "latin":
        a = rng.choice(LATINISH)
        b = rng.choice(LATINISH)
        return a if rng.random() < 0.35 else f"{a} {b}"

    if scheme == "place":
        # Port Helios / New Haven / Fort Umbra etc.
        left = rng.choice(PLACE_PREFIX)
        right = rng.choice(MYTHIC + LATINISH + PLACE_SUFFIX)
        return f"{left} {right}"

    # synthetic
    return make_pronounceable(rng)

def planet_display_name( *, rng, system_name: str, idx: int, habitable: bool, used: set[str], force_name: bool = False) -> dict:
    """
    Returns BOTH:
    - designation: always present (real astronomy feel)
    - name: sometimes present (proper/common name)
    """
    designation = planet_designation(system_name, idx)

    # Decide if this world gets a proper name
    # (habitable more likely; gas giants less likely, etc. handled elsewhere if you want)
    name_chance = 0.85 if habitable else 0.60
    give_name = force_name or (rng.random() < name_chance)

    name = None
    if give_name:
        for _ in range(20):
            candidate = proper_planet_name(rng, habitable)
            if candidate not in used:
                name = candidate
                used.add(candidate)
                break

    return {"designation": designation, "name": name}