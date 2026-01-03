from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def render_galaxy_map_png(galaxy_data: dict, label_all: bool = True) -> bytes:
    r = float(galaxy_data["radius_ly"])
    systems = galaxy_data["systems"]

    xs = [s["x_ly"] for s in systems]
    ys = [s["y_ly"] for s in systems]
    names = [s["name"] for s in systems]

    fig = plt.figure(figsize=(7, 7), dpi=160)
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter([0], [0], marker="x", s=80)   # core
    ax.scatter(xs, ys, s=14)

    ax.set_xlim(-r, r)
    ax.set_ylim(-r, r)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(f"Galaxy Map (Top-Down) — radius {int(r):,} ly")
    ax.set_xlabel("X (ly)")
    ax.set_ylabel("Y (ly)")

    circle = plt.Circle((0, 0), r, fill=False, linewidth=1)
    ax.add_patch(circle)

    if label_all:
        # small text + slight offset so labels don't sit on the point
        for x, y, n in zip(xs, ys, names):
            ax.annotate(n, (x, y), textcoords="offset points", xytext=(4, 3), fontsize=6)

    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    return buf.getvalue()

def render_system_orbits_png(system: dict) -> bytes:
    planets = system["planets"]

    # orbit distances in AU
    orbits = [p["orbit_au"] for p in planets]
    labels = []
    for p in planets:
        # prefer proper name; fallback to designation if present; else name
        labels.append(p.get("name") or p.get("designation") or "Planet")

    # Use log scale so outer planets don't compress everything
    fig = plt.figure(figsize=(8, 1.8), dpi=160)
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter([0.05], [0], marker="*", s=80)  # star marker slightly >0 for log scale friendliness

    # Plot planets along a line (y=0)
    for i, p in enumerate(planets):
        x = max(0.05, float(p["orbit_au"]))
        h = p.get("habitability", "not")
        marker = "o" if h == "habitable" else ("s" if h == "possibly" else "x")
        ax.scatter([x], [0], marker=marker, s=55)
        ax.annotate(labels[i], (x, 0), textcoords="offset points", xytext=(0, 10), ha="center", fontsize=6)

    ax.set_xscale("log")
    ax.set_yticks([])
    ax.set_xlabel("Orbit distance (AU, log scale)")
    ax.set_title(f"{system['name']} — Planetary Orbits")

    # add a little padding
    xmin = 0.05
    xmax = max(0.5, max(orbits) * 1.25)
    ax.set_xlim(xmin, xmax)

    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    return buf.getvalue()