import random
import math
from .names import system_designation, planet_display_name

def _rand_range(rng, a, b):
    return a + (b - a) * rng.random()

SIZE_GROUPS = {
    "dwarf": (1000, 10000),
    "small": (10000, 25000),
    "mw": (25000, 60000),
    "large": (60000, 120000),
    "giant": (120000, 240000),
}

STAR_TYPE_WEIGHTS = [
    ("M", 0.55),
    ("K", 0.20),
    ("G", 0.12),
    ("F", 0.08),
    ("A", 0.04),
    ("B", 0.01),
]

def pick_weighted(rng, weighted):
    roll = rng.random() * sum(w for _, w in weighted)
    upto = 0.0
    for item, w in weighted:
        upto += w
        if roll <= upto:
            return item
    return weighted[-1][0]

def star_mass_luminosity(rng, stype):
    ranges = {
        "M": (0.08, 0.45),
        "K": (0.45, 0.80),
        "G": (0.80, 1.04),
        "F": (1.04, 1.40),
        "A": (1.40, 2.10),
        "B": (2.10, 16.0),
    }
    mmin, mmax = ranges[stype]
    mass = _rand_range(rng, mmin, mmax)
    lum = mass ** 3.5
    return mass, lum

def habitable_zone_au(lum):
    inner = 0.95 * math.sqrt(lum)
    outer = 1.67 * math.sqrt(lum)
    return inner, outer

def generate_galaxy(size_group: str, systems_count: int, seed: int | None = None):
    rng = random.Random(seed if seed is not None else random.randrange(1, 2_000_000_000))
    final_seed = rng.randrange(1, 2_000_000_000) if seed is None else seed
    rng = random.Random(final_seed)

    rmin, rmax = SIZE_GROUPS[size_group]
    radius_ly = rng.randint(rmin, rmax)

    core_type = rng.choice(["Super Massive Black Hole", "Super Star Cluster"])
    if size_group in ("dwarf", "small"):
        core_mass = 10 ** _rand_range(rng, 5, 7)
    elif size_group in ("mw", "large"):
        core_mass = 10 ** _rand_range(rng, 6, 8.5)
    else:
        core_mass = 10 ** _rand_range(rng, 7, 9.5)
    r_scale = radius_ly / 3.0
    z_scale = max(50, radius_ly / 200)

    systems = []
    for i in range(systems_count):
        u = max(1e-9, rng.random())
        r = -r_scale * math.log(u)
        r = min(r, radius_ly)
        theta = _rand_range(rng, 0, math.tau)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = rng.gauss(0, z_scale)
        dist_core = math.sqrt(x*x + y*y + z*z)
        stype = pick_weighted(rng, STAR_TYPE_WEIGHTS)
        smass, lum = star_mass_luminosity(rng, stype)
        hz_in, hz_out = habitable_zone_au(lum)

        sys_name = system_designation(rng)

        planets = generate_planets(
            rng=rng,
            hz_in=hz_in,
            hz_out=hz_out,
            star_type=stype,
            system_name=sys_name,
        )

        systems.append({
            "name": sys_name,
            "x_ly": round(x, 1),
            "y_ly": round(y, 1),
            "z_ly": round(z, 1),
            "distance_from_core": round(dist_core, 4),
            "star_type": stype,
            "star_mass_solar": round(smass, 4),
            "luminosity_solar": round(lum, 4),
            "hz_inner_au": round(hz_in, 4),
            "hz_outter_au": round(hz_out, 4),
            "planets": planets,
        })

    return {
        "seed": final_seed,
        "size_group": size_group,
        "radius_ly": radius_ly,
        "core_type": core_type,
        "core_mass_solar": float(core_mass),
        "systems": systems,
    }

def generate_planets(*, rng, hz_in, hz_out, star_type, system_name: str):
    planet_count = rng.randint(3, 12)
    min_named = max(1, planet_count // 2)
    named_count = 0
    planets = []
    used_names = set()
    
    a = 0.15 if star_type == "M" else 0.3

    for idx in range(planet_count):
        if idx > 0:
            a *= _rand_range(rng, 1.4, 2.2)

        e = min(0.6, abs(rng.gauss(0.08, 0.06)))

        if  a < hz_in:
            ptype = rng.choices(["rocky", "super-earth", "airless"], weights=[0.55, 0.25, 0.2])[0]
        elif hz_in <= a <= hz_out:
            ptype = rng.choices(["rocky", "super-earth"], weights=[0.75, 0.25])[0]
        elif a < hz_out * 3:
            ptype = rng.choices(["ice", "mini-neptune", "gas-giant"], weights=[0.55, 0.25, 0.2])[0]
        else:
            ptype = rng.choices(["gas-giant", "ice"], weights=[0.65, 0.35])[0]

        mass_e, radius_e = planet_mass_radius(rng, ptype)
        atmosphere = planet_atmosphere(rng, ptype)
        water = planet_water(rng, ptype, a, hz_in, hz_out)

        score, temp_c, reasons = habitability_score(rng, ptype, mass_e, e, atmosphere, water, a, hz_in, hz_out, star_type)
        if score >= 4:
            habitability = "habitable"
        elif score >= 2:
            habitability = "possibly"
            if "no atmosphere (requires sealed habitats)" in reasons or "toxic atmosphere (requires sealed habitats)" in reasons:
                pass
            else:
                reasons.append("surface is survivable short-term, but long-term living needs sealed habitats")
        else:
            habitability = "not"
        
        force_name = named_count < min_named

        name_bits = planet_display_name(
            rng=rng,
            system_name=system_name,
            idx=idx,
            habitable=habitability,
            used=used_names,
            force_name=force_name,
        )
        
        planets.append({
            "name": name_bits["name"],
            "designation": name_bits["designation"],
            "orbit_au": round(a, 2),
            "eccentricity": round(e, 2),
            "type": ptype,
            "mass_earth": round(mass_e, 2),
            "radius_earth": round(radius_e, 2),
            "atmosphere": atmosphere,
            "water": water,
            "temperature_c": round(temp_c, 1),
            "habitability": habitability,
            "habitable": habitability == "habitable",
            "possibly_habitable": habitability == "possibly",
            "habitability_reasons": reasons,
            "description": planet_description(rng, ptype, atmosphere, water, habitability),
        })

        if name_bits["name"]:
            named_count += 1

    return planets

def planet_mass_radius(rng, ptype):
    if ptype == "rocky":
        m = _rand_range(rng, 0.3, 2.0)
        r = m ** 0.28
    elif ptype == "super-earth":
        m = _rand_range(rng,2.0 , 10.0)
        r = m ** 0.25
    elif ptype == "airless":
        m = _rand_range(rng, 0.1, 1.5)
        r = m ** 0.28
    elif ptype == "ice":
        m = _rand_range(rng, 0.2, 5.0)
        r = m ** 0.26
    elif ptype == "mini-neptune":
        m = _rand_range(rng, 5.0, 20.0)
        r = _rand_range(rng, 1.8, 3.5)
    else:
        m = _rand_range(rng, 30.0, 300.0)
        r = _rand_range(rng, 8.0, 14.0)
    return m, r

def planet_atmosphere(rng, ptype):
    if ptype in ("gas-giant", "mini-neptune"):
        return rng.choice(["thick", "stormy", "toxic"])
    if ptype == "airless":
        return "none"
    return rng.choices(["thin", "earthlike", "thick", "toxic"], weights=[0.35, 0.35, 0.2, 0.1])[0]

def planet_water(rng, ptype, a, hz_in, hz_out):
    if ptype in ("gas-giant", "mini-neptune"):
        return rng.choice(["none", "ice"])

    if a < hz_in:
        return rng.choices(["none", "trace"], weights=[0.8, 0.2], k=1)[0]

    if hz_in <= a <= hz_out:
        return rng.choices(["ocean", "mixed", "none"], weights=[0.35, 0.45, 0.20], k=1)[0]

    return rng.choices(["ice", "none", "subsurface"], weights=[0.6, 0.25, 0.15], k=1)[0]

def habitability_score(rng, ptype, mass_e, e, atmosphere, water, a, hz_in, hz_out, star_type):
    score = 0
    reasons = []

    in_hz = hz_in <= a <= hz_out
    near_hz = (hz_in * 0.85) <= a <= (hz_out * 1.15)

    if in_hz:
        score += 4
        reasons.append("in the habitable zone")
    elif near_hz:
        score += 2
        reasons.append("near the habitable zone")
    else:
        reasons.append("outside the habitable zone")

    if ptype in ("rocky", "super-earth"):
        score += 3
    elif ptype in ("gas-giant", "mini-neptune"):
        score -= 2
        reasons.append("not a solid surface world")

    if 0.5 <= mass_e <= 5:
        score += 2
    elif mass_e < 0.2:
        score -= 1
        reasons.append("too low gravity to retain a stable atmosphere")
    elif mass_e > 10:
        score -= 1
        reasons.append("very high gravity complicates surface habitation")

    if e < 0.15:
        score += 1
    elif e > 0.35:
        score -= 1
        reasons.append("highly eccentric orbit causes extreme seasons")

    if star_type == "M":
        score -= 1
        reasons.append("active red dwarf star (flare/radiation risk)")

    if atmosphere == "earthlike":
        score += 2
        reasons.append("breathable-like atmosphere")
    elif atmosphere == "none":
        score -= 2
        reasons.append("no atmosphere (requires sealed habitats)")
    elif atmosphere == "toxic":
        score -= 2
        reasons.append("toxic atmosphere (requires sealed habitats)")
    elif atmosphere == "thick":
        score -= 1
        reasons.append("thick atmosphere / greenhouse risk")
    elif atmosphere == "thin":
        reasons.append("thin atmosphere (pressure suits or sealed habitats likely)")

    if water in ("ocean", "mixed"):
        score += 2
        reasons.append("liquid water present")
    elif water == "none":
        score -= 1
        reasons.append("no accessible water (imports/processing required)")
    elif water in ("ice", "subsurface"):
        reasons.append("water likely locked as ice/subsurface (extractable)")

    # rough temperature estimate (same as before)
    hz_center = (hz_in + hz_out) / 2
    rel = (hz_center / a) ** 0.5
    temp = 288 * rel - 273.15  # C

    if atmosphere == "thick":
        temp += 20
    elif atmosphere == "thin":
        temp -= 10
    elif atmosphere == "none":
        temp -= 25

    # Add a plain-English temp reason
    if temp < -40:
        reasons.append("extreme cold (HAB life support required)")
    elif temp > 50:
        reasons.append("extreme heat (HAB cooling required)")

    return score, temp, reasons

def planet_description(rng, ptype, atmosphere, water, habitability: str):
    if isinstance(water, list):
        water = water[0] if water else "none"
    if isinstance(atmosphere, list):
        atmosphere = atmosphere[0] if atmosphere else "thin"
    hooks = [
        "frequent auroras arc across the night side",
        "a massive moon dominates the sky",
        "volcanic chains stitch the equator",
        "ancient impact basins form the inland seas",
        "shimmering crystaline plains spread for thousands of kilometers",
        "violent seasonal storms migrate between hemispheres",
        "a thin ring system is visible at dawn and dusk",
    ]
    climates = {
        "none": "an airless, silent surface",
        "thin": "a thin, whispering atmosphere",
        "earthlike": "a breathable, dynamic atmosphere",
        "thick": "a dense greenhouse atmosphere",
        "toxic": "a corrosive, tocix atmosphere",
        "stormy": "a churning atmosphere of colossal storms",
    }
    waters = {
        "none": "no stable surface water",
        "trace": "only trace water locked in shadowed craters",
        "mixed": "scattered seas and broad continents",
        "ocean": "a global ovean broken by island chains",
        "ice": "ice sheets and frozen oceans",
        "subsurface": "a subsurface ocean beneath kilometers of ice",
    }
    if habitability == "habitable":
        vibe = "promising for open-air settlement"
    elif habitability == "possibly":
        vibe = "habitable only in sealed habitats (HABs/domescapes)"
    else:
        vibe = "hostile to unprotected life"
    return f"{ptype.replace('-', ' ' ).title()} world with {climates.get(atmosphere, atmosphere)} and {waters.get(water, water)}; {vibe}, with {rng.choice(hooks)}."